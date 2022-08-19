import base64
import urllib

import requests
from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playscript.conv.fountain import psc_from_fountain
from playscript.conv.json import psc_loads, psc_dumps
from playscript.conv.pdf import psc_to_pdf
from playscript.conv.html import psc_to_html
from reportlab.lib.pagesizes import A4, A5


class PdfParams(BaseModel):
    """Request query parameters to make pdf
    """
    size: tuple = None            # TODO: validation maybe needed.
    margin: tuple = None          # TODO: validation maybe needed.
    upper_space: float = None
    font_name: str = None
    num_font_name: str = None
    font_size: float = None
    line_space: float = None
    draw_page_num: bool = None


def build_pdf_params(pdf_params: PdfParams) -> dict:
    """Build parameters to make pdf from query parameters
    """
    params = {}
    if not pdf_params:
        return params
    if (pdf_params.size is not None):
        params['size'] = pdf_params.size
    if (pdf_params.margin is not None):
        params['margin'] = pdf_params.margin
    if (pdf_params.upper_space is not None):
        params['upper_space'] = pdf_params.upper_space
    if (pdf_params.font_name is not None):
        params['font_name'] = pdf_params.font_name
    if (pdf_params.num_font_name is not None):
        params['num_font_name'] = pdf_params.num_font_name
    if (pdf_params.font_size is not None):
        params['font_size'] = pdf_params.font_size
    if (pdf_params.line_space is not None):
        params['line_space'] = pdf_params.line_space
    if (pdf_params.draw_page_num is not None):
        params['draw_page_num'] = pdf_params.draw_page_num
    return params


class HtmlParams(BaseModel):
    title: str = None
    template: str = None
    css: str = None
    js: str = None


def build_html_params(html_params: HtmlParams):
    params = {}
    if not html_params:
        return params
    if (html_params.title is not None):
        params['title'] = html_params.title
    if (html_params.template is not None):
        params['template'] = html_params.template
    if (html_params.css is not None):
        params['css'] = html_params.css
    if (html_params.js is not None):
        params['js'] = html_params.js
    return params


class SrcData(BaseModel):
    data: str
    pdf_params: PdfParams = {}
    html_params: HtmlParams = {}


class DestData(BaseModel):
    format: str
    data: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post("/")
async def root():
    raise HTTPException(status_code=404, detail='Not found')


@app.post("/conv")
async def conv(
    data: SrcData,
    from_: str = Query(default='json', alias='from', regex='json|fountain'),
    to: str = Query(default='json', regex='json|pdf|html'),
):
    data_str = data.data

    # Convert into Psc
    if from_ == 'fountain':
        psc = psc_from_fountain(data_str)
    else:  # from json
        psc = psc_loads(data_str)

    # Convert into specified format and return it
    if to == 'pdf':
        pdf_params = build_pdf_params(data.pdf_params)
        pdf = psc_to_pdf(psc, **pdf_params)
        return DestData(
            format='pdf',
            data=base64.encodebytes(pdf.read()),
        )
    elif to == 'html':
        html_params = build_html_params(data.html_params)
        html = psc_to_html(psc, **html_params)
        return DestData(format='html', data=html)
    else:  # to json
        return DestData(format='json', data=psc_dumps(psc))


http_bad_gateway = HTTPException(status_code=502, detail='Bad Gateway')
http_gateway_timeout = HTTPException(status_code=504, detail='Gateway Timeout')


@app.get("/load")
async def load(
    src: str,
    format: str = Query(default='fountain', regex='json|fountain'),
    as_: str = Query(
        default='pscv', alias='as', regex='pscv|json|pdf|html'),
    size: str = Query(default='A5', regex='A[45]'),
):
    try:
        r = requests.get(src)
    except requests.exceptions.Timeout:
        raise http_gateway_timeout
    except requests.exceptions.RequestException:
        raise http_bad_gateway

    if r.status_code != 200:
        raise http_bad_gateway

    # Convert into Psc
    if format == 'fountain':
        psc = psc_from_fountain(r.text)
    else:  # from json
        psc = psc_loads(r.text)

    # Return data to load
    if as_ == 'pscv':
        data = '{"psc": ' + psc_dumps(psc) + '}'
        return Response(content=data, media_type="application/json")
    elif as_ == 'pdf':
        if size == 'A4':
            pdf_size = A4
        else:
            pdf_size = A5
        pdf = psc_to_pdf(psc, size=pdf_size).read()
        filename = urllib.parse.quote(psc.title) + '.pdf'
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'}
        return Response(
            content=pdf, headers=headers, media_type="application/pdf")
    elif as_ == 'html':
        html = psc_to_html(psc)
        return Response(content=html, media_type="text/html")
    else:  # as json
        data = psc_dumps(psc)
        return Response(content=data, media_type="application/json")
