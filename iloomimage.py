import streamlit as st
import requests
import zipfile
from io import BytesIO
from selenium.webdriver.common.by import By

# 사이트별 URL 템플릿
SITE_URLS = {
    'iloom': 'https://www.iloom.com/product/detail.do?productCd={}',
    'bacci': 'https://bacci-bfc.com/product/detail.html?product_no={}'
}

# 이미지 추출 함수
def extract_images(site, product_code, driver):
    url = SITE_URLS[site].format(product_code)
    driver.get(url)

    if site == 'iloom':
        image_elements = driver.find_elements(By.CSS_SELECTOR, 'img[src*="product"]')
    elif site == 'bacci':
        image_elements = driver.find_elements(By.CSS_SELECTOR, 'img[src*="product"]')
    else:
        st.error("지원하지 않는 사이트입니다.")
        return None, None

    image_urls = [img.get_attribute('src') for img in image_elements if img.get_attribute('src').startswith('http')]
    return url, image_urls

# 이미지 다운로드 및 ZIP 파일 생성 함수
def download_images(image_urls, product_code):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for idx, img_url in enumerate(image_urls):
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                img_response = requests.get(img_url, headers=headers)
                if img_response.status_code == 200:
                    img_data = img_response.content
                    img_name = f"{product_code}_{idx+1}.jpg"
                    zip_file.writestr(img_name, img_data)
                else:
                    st.warning(f"이미지를 다운로드할 수 없습니다: {img_url}, 상태 코드: {img_response.status_code}")
            except Exception as e:
                st.warning(f"이미지를 다운로드할 수 없습니다: {img_url}, 오류: {e}")
    zip_buffer.seek(0)
    return zip_buffer

# Streamlit UI 구성
st.title("제품 이미지 다운로드 도구")
st.sidebar.header("Detail Image Helper (iloom & bacci)")

# 사이트 선택
site = st.selectbox("사이트를 선택하세요:", ['iloom', 'bacci'])

# 제품 코드 입력
product_code = st.text_input("제품 코드를 입력하세요:")

# 이미지 다운로드 버튼
if st.button("이미지 다운로드"):
    if not product_code:
        st.error("제품 코드를 입력해주세요.")
    else:
        driver = create_driver()
        page_url, image_urls = extract_images(site, product_code, driver)
        driver.quit()
        if image_urls:
            zip_buffer = download_images(image_urls, product_code)
            st.success(f"{len(image_urls)}개의 이미지를 찾았습니다.")
            st.markdown(f"[{product_code} 제품 페이지]({page_url})")
            st.download_button(
                label="이미지 ZIP 파일 다운로드",
                data=zip_buffer,
                file_name=f"{product_code}_images.zip",
                mime='application/zip'
            )
        else:
            st.error("이미지를 찾을 수 없거나 페이지를 불러올 수 없습니다.")
