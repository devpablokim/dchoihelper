import streamlit as st
import requests
from bs4 import BeautifulSoup
import zipfile
from io import BytesIO

# 사이트별 URL 템플릿
SITE_URLS = {
    'iloom': 'https://www.iloom.com/product/detail.do?productCd={}',
    'bacci': 'https://bacci-bfc.com/product/detail.html?product_no={}'
}

# 이미지 추출 함수
def extract_images(site, product_code):
    url = SITE_URLS[site].format(product_code)
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error(f"페이지를 불러올 수 없습니다: 상태 코드 {response.status_code}")
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')

    if site == 'iloom':
        image_elements = soup.find_all('img', src=True)
    elif site == 'bacci':
        image_elements = soup.find_all('img', src=True)
    else:
        st.error("지원하지 않는 사이트입니다.")
        return None, None

    image_urls = [img['src'] for img in image_elements if 'product' in img['src']]
    return url, image_urls

# 이미지 다운로드 및 ZIP 파일 생성 함수
def download_images(image_urls, product_code):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for idx, img_url in enumerate(image_urls):
            try:
                if not img_url.startswith('http'):
                    img_url = 'https:' + img_url
                headers = {'User-Agent': 'Mozilla/5.0'}
                img_response = requests.get(img_url, headers=headers)
                if img_response.status_code == 200:
                    img_data = img_response.content
                    img_name = f"{product_code}_{idx+1}.jpg"
                    zip_file.writestr(img_name, img_data)
                else:
                    st.warning(f"
::contentReference[oaicite:9]{index=9}
 
