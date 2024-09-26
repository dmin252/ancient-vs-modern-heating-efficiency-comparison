from PIL import Image
import json

def process_image(file_path):
    # Open the image
    # 이미지 열기
    with Image.open(file_path) as img:
        # Print the original size of the image
        # 원본 이미지 크기 출력
        print("Original size:", img.size)
        
        # Resize the image to half of its original size
        # 이미지 크기를 1/2로 조정
        new_size = (img.width // 2, img.height // 2)
        resized_img = img.resize(new_size)
        
        # Extract image data as a list of pixel values
        # 이미지 데이터를 리스트로 추출
        pixels = list(resized_img.getdata())
        
        # Convert image data to JSON format
        # 이미지 데이터를 JSON으로 변환
        json_data = json.dumps({
            "width": resized_img.width,
            "height": resized_img.height,
            "pixels": pixels
        })
        
        # Print the JSON data
        # 결과 출력
        print(json_data)

        # Save the JSON data to a file named 'output.json'
        # JSON 파일로 저장
        with open('output.json', 'w') as json_file:
            json_file.write(json_data)

# Provide the path to the BMP file
process_image('old.bmp')
