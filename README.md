## :book: 가계부

> accounts

- [모델링](https://iamthejiheee.tistory.com/78)

![image-20230105154416134](README.assets/image-20230105154416134.png)

- 비밀번호 암호화

![image-20230105153957786](README.assets/image-20230105153957786.png)

- [serializer의 create](https://www.django-rest-framework.org/tutorial/1-serialization/)

![image-20230105153154203](README.assets/image-20230105153154203.png)

> ERD

![image-20230105031741816](README.assets/image-20230105031741816.png)

> [3-f. 가계부의 세부 내역을 복제할 수 있습니다.](https://docs.djangoproject.com/en/3.2/topics/db/queries/#copying-model-instances)

> [3-g. 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다](https://ninano1109.tistory.com/63)
>
> 블로그 보면서 비슷하게 구현함
>
> 사실 문제 자체를 정확히 이해하지 못했는데, 
> front 쪽에서의 가계부 세부 내역 url을 보내면 단축 url을 return해주는 것이라고 이해하고 함수를 만들었다.
>
> 여기서 문제가 될만한 것은
>
> 1. 여러 요청들에 대해서 url이 겹치지 않게 할 수 있는지 잘 모르겠다는 것 => 일단 sha256(기존url+현재시간)[:8]로 함
> 2. 가계부이기 때문에 원래는 세부 내역 조회에 대해서도 본인만 볼 수 있게 조건문을 걸어뒀었는데, 그러면 단축 url을 줬을 때 다른 사람이 못보니까 풀었다.
> 3. 내가 만든게 단축 url이라고 말할 수 있을만큼 짧은지 잘 모르겠다.



> 남은 일

- model 제한조건 (month min-max같은 거)
- refresh 토큰으로 access 반환하는 함수만들기
- 각 api 로그인 여부 확인
- testcase 작성
- jwt 설정
- cors

