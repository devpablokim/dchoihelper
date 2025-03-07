import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import zipfile
from io import BytesIO

# 함수: 제품 코드로부터 이미지 URL 리스트 추출
def fetch_image_urls(product_code):
    base_url = "https://www.iloom.com/product/detail.do?productCd="
    url = f"{base_url}{product_code}"
    response = requests.get(url)
    if response.status_code != 200:
        st.error("제품 페이지에 접근할 수 없습니다.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.find_all('img')
    image_urls = [img['src'] for img in image_tags if 'src' in img.attrs and img['src'].startswith('http')]
    return image_urls

# 함수: 이미지들을 ZIP 파일로 압축
def create_zip(image_urls):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for url in image_urls:
            try:
                image_response = requests.get(url)
                if image_response.status_code == 200:
                    image_name = os.path.basename(url)
                    zip_file.writestr(image_name, image_response.content)
            except Exception as e:
                st.warning(f"이미지 다운로드 실패: {url} - {e}")
    zip_buffer.seek(0)
    return zip_buffer

# Streamlit 인터페이스 구성
def main():
    # 사이드바 로고
    st.sidebar.title("dchoi09 Detail Image Helper (iloom)")

    # 제품 코드 입력 및 버튼
    st.title("제품 이미지 다운로드")
    product_code = st.text_input("제품코드를 입력하세요:")
    if st.button("이미지 다운로드"):
        if product_code:
            with st.spinner("이미지 URL을 가져오는 중..."):
                image_urls = fetch_image_urls(product_code)
            if image_urls:
                st.success(f"총 {len(image_urls)}개의 이미지를 찾았습니다.")
                with st.spinner("이미지를 다운로드하여 ZIP 파일로 압축하는 중..."):
                    zip_buffer = create_zip(image_urls)
                st.download_button(
                    label="이미지 ZIP 파일 다운로드",
                    data=zip_buffer,
                    file_name=f"{product_code}_images.zip",
                    mime="application/zip"
                )
            else:
                st.error("이미지를 찾을 수 없습니다.")
        else:
            st.warning("제품코드를 입력해주세요.")

if __name__ == "__main__":
    main()
