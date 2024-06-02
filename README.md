# ImageToText
Program to extract tax from images using Azure Ai and Chat-gpt

- 프로그램을 만든 이유 -
  해당 프로그램을 만든 이유는 강의자료들이 모두 영어인 과목이 많이 있다.
  그리고, 그 강의자료들은 pdf 형식이 많고, 텍스트를 복사할 수 없는 부분도 많이 있다.
  이를 해결하고자, 이미지를 캡쳐해서 번역을 하고, chat-gpt에 물어볼 수 있는 도구를 만들고자 하였다.


- 프로그램에 사용된 기술 -

1. Chat-gpt 3.5 Turbo
   - chat-gpt 3.5를 이용해서 이미지에서 추출한 텍스트를 이용해서 한번 더 정보를 가공해서 보여준다
  
2. Azure AI Translator
   - Azure AI Translator를 이용해서 이미지에서 추출한 영어 텍스트를 한국어로 번역한다.

3. opencv 와 pytesseract를 이용해서 이미지에서 텍스트 추출을 한다.


- 프로그램 사용법 -

1. 프로그램을 실행한 후 캡쳐 도구가 나올 때까지 기다린다(조금 늦게 나올 수 있음)

2. 원하는 텍스트를 캡쳐한 후 Dialog 박스가 나올 때까지 기다린다.

3. 프로그램이 종료된 후 텍스트 파일로 내용이 잘 저장되었는지 확인한다.

- 프로그램 시연 -

![test01](https://github.com/Hongyooungi/ImageToText/assets/127743990/cd54d7a7-464c-4074-a7f5-7aa9f4d51c89)


![test02](https://github.com/Hongyooungi/ImageToText/assets/127743990/5cbcce1b-d4e7-42a4-b3d1-07b7b163c397)


![test03](https://github.com/Hongyooungi/ImageToText/assets/127743990/4993760a-8d5f-4b70-8e1b-fc79ea461f35)


![test04](https://github.com/Hongyooungi/ImageToText/assets/127743990/1f353ce7-6605-463c-b1d5-a24b6c236dff)


![test05](https://github.com/Hongyooungi/ImageToText/assets/127743990/83870858-34d9-4d0d-98bb-d37a6a39c77c)

출처 및 도움
 - chat-gpt
