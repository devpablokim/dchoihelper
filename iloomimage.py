import streamlit as st
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import zipfile
from io import BytesIO

# 사이트별 URL 템플릿
SITE_URLS = {
    'iloom': 'https://www.iloom.com/product/detail.do?productCd={}',
    'bacci': 'https://bacci-bfc.com/product/detail.html?product_no={}'
}

# Selenium WebDriver 설정
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# 이미지 추출 함수
def extract_images(site, product_code, driver):
    url = SITE_URLS[site].format(product_code)
    driver.get(url)
    try:
        # 페이지 로딩 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'img'))
        )
        # 이미지 요소 추출
        image_elements = driver.find_elements(By.TAG_NAME, 'img')
        image_urls = [img.get_attribute('src') for img in image_elements if 'product' in img.get_attribute('src')]
        return url, image_urls
    except Exception as e:
        st.error(f"이미지를 추출하는 중 오류가 발생했습니다: {e}")
        return None, None

# 이미지 다운로드 및 ZIP 파일 생성 함수
def download_images(image_urls, product_code, driver):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for idx, img_url in enumerate(image_urls):
            try:
                # 이미지 다운로드를 위해 새로운 탭에서 이미지 로드
                driver.execute_script(f"window.open('{img_url}', '_blank');")
                driver.switch_to.window(driver.window_handles[1])
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'img'))
                )
                img_element = driver.find_element(By.TAG_NAME, 'img')
                img_data = img_element.screenshot_as_png
                img_name = f"{product_code}_{idx+1}.png"
                zip_file.writestr(img_name, img_data)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except Exception as e:
                st.warning(f"이미지를 다운로드할 수 없습니다: {img_url}, 오류: {e}")
    zip_buffer.seek(0)
    return zip_buffer

# Streamlit UI 구성
st.title("제품 이미지 다운로드 도구")
st.sidebar.header("dchoi09 Detail Image Helper (iloom & bacci)")

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
        if image_urls:
            zip_buffer = download_images(image_urls, product_code, driver)
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
        driver.quit()
