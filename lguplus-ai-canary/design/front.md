# NLP 프론트 서버 연동 규격서

-----
[Change History]
- 0.1 초기 버전 ( 윤기현<gih2yun@mindslab.ai>)
- 0.2 협의내용 반영 ( 박병환<bhpark0424@mindslab.ai>, 윤기현<gih2yun@mindslab.ai>)
- 0.3 협의내용 반영 및 오탈자 수정 ( 박병환 <bhpark0424@mindslab.ai>)

## 용어정리
- SCS LGU+ Platform 1.0에서 NLG, NLU를 호출하는 구조
- IWF IWF 호출하는 구조
- 통합NLP: 마인즈랩이 제공하는 QA NLP를 포함하고 LGE NLP와 통합인터페이스를 제공한다.
- LGE NLP:
- QA: QA 서브시스템
- skill: 대화 도메인
- intent: 대화의 의도
- slot: 대화 진행에 필요한 파라미터들

### 약어 정리
- CL = classifer
- DA = dialog agent
- SYS = system
- NET = network
- DM = LGE dialog manager
- SDS = mindslab spoken dialog system
- EB = exobrain
- MRC = machine reading comprehention
- HPN = hyper net
- BOT = mindslab chatbot
- DB = database error
- EX = external system

## 공통 사항

- protocol prefix: /nlpapi/v1/
- header-prefix: 'X-nlp-"
- 데이터 전송 규칙은 JSON 포맷이다. MINDSLAB의 NLP는 google protobuf version 3를 이용하여
JSON 데이터를 `Message`로 디코딩하고 반대로 `Message`를 JSON 객체로 인코딩 하므로
추가적인 공통 규칙이 존재한다.

### JSON 전송에 대한 공통 규칙
- 기본값은 보내지 않아도 된다. 다음의 경우는 기본값이다.
  - string : ""
  - int32, int64 등 number: 0
  - bool: false
  - enum: 첫번째 정의된 값, 값은 0이어야 한다.
  - array: empty
  - Object의 경우 비어있는 경우, {}로 전송
- ENUM 타입의 경우에는 JSON 포맷 규칙에 따라서 숫자가 아닌 문자열로 전송
  - 예) { "input_type": "KBD" }
- BYTES: BASE64로 인코딩하여 전송

### 공통 메시지 규격
- 필드 이름은 단어 단위로 구분하고 구분된 단어 사이는 "_"로 표기한다. camelCase를 사용하지 않는다.
- "Key Value"를 전송할 때는 반드시 객체를 정의하여 전송한다. 즉, 임의대로 원문 메시지를 확장하지 않는다.
- 잘못된 확장, 원메시지의 임의의 JSON 필드 삽입
```json
{
  "str_field": "value1",
  "num_field": 1234,
  "bool_field": true,
  "key1": "extended value1",
  "key2": "extended value2",
  "key3": "extended value3"
}
```
- 확장할 때에는 반드시 객체를 정의하고 확장용 데이터를 정의한다.
  - proto 샘플에서는 "meta" 필드를 쓰도록 권장한다. 필요한 경우 적절한 네이밍을 쓰도록 할 수 있다.
  
```json
{
  "str_field": "value1",
  "num_field": 1234,
  "bool_field": true,
  "meta": {
    "key1": "extended value1",
    "key2": "extended value2",
    "key3": "extended value3"
  }
}

```
- 자세한 규칙은 구글 스타일 가이드에 따른다. https://developers.google.com/protocol-buffers/docs/style


### 공통 메시지

#### Timestamp
- 시간값은 오류를 없애기 위해서 UTC를 기준으로 입력되어야 한다.
- 한국이 아닌 곳에서 사용할 수 있다.
- YYMMDD 형식은 위험하므로 사용하지 않는다.

No.|Item|Type|Description|Default Value|Mandatory
---|----|----|-----------|-------------|---------
1  |seconds | int64 | UTC, from unix epoch | None | M
2  |nanos   | int64 | UTC, from unix epoch | None | O


```proto

// timestamp
// timestamp를 쓰는 이유는 지역에 상관없이
// 정확한 시간을 계산해 내기 위함.
message Timestamp {
  int64 seconds = 1; // UTC, from unix epoch
  int32 nanos = 2;   // 0 ~ 999,999,999 까지
}
```

#### TpoContext 객체
- TPO를 위한 기본 정보를 사용한다.
- 필요한 추가 데이터는 meta를 사용할 수 있다.

No.|Item|Type|Description|Default Value|Mandatory
---|----|----|-----------|-------------|---------
1  |time | string | 시간을 나타내는 자연어 문자열 | None | O
2  |place | string | 장소를 나타내는 자연어 문자열, 기존의 location | None | O
3  |user_key | string | 사용자를 구분하는 키 | None | M
4  |meta | Struct | 사용자에 대한 세부 정보 | None | M

```proto
// 위치정보, 사용자정보,
message TpoContext {
  string time = 1;
  string place = 2;
  string user_key = 3;
  Struct meta = 4;
}
```

#### Device 객체
- 장치
- 장치의 이름을 검사하는 유효성은 포함하고 있지 않고, 정상적인 장치 이름이 올라온다고
  가정한다.

No.|Item|Type|Description|Default Value|Mandatory
---|----|----|-----------|-------------|---------
1  |type | string | 장비 이름 | None | M
2  |model | string | 모델 번호 | None | M
3  |no | string | 장비의 고유 번호 | None | M
4  |timestamp | Timestamp | 디바이스에서 보내주는 시간 | None | M


```proto
// 디바이스 정보
message Device {
  string type = 1;
  string model = 2;
  string no = 3;
  Timestamp timestamp = 4;
  Struct meta = 5;
}
```

#### UtterInputType enum
- 입력 타입
- 사용자의 입력의 유형에 따른 복잡한 분기를 위해서 사용됨.

No.|Name | Value |Description
---|-----|-------|-----------
1  |SPEECH | 0, 기본값| STT를 경유하여 텍스트로 변환된 텍스트임
2  |KBD | 1| 사용자의 키보드 입력을 통해서 변환된 텍스트임
3  |IMAGE | 2| 이미지 Annotation을 통해서 변환된 텍스트임
4  |VIDEO | 3| 비디오 Annotation을 통해서 변환된 텍스트임
5  |SIGNAL | 100| 기타 장치에서 코드나 로직에 의해서 메시지를 <br> 전달하기 위한 입력

```proto
// 사용자의 입력 유형
enum UtterInputType {
  SPEECH = 0;     // STT를 통한 입력
  KBD = 1;        // 사용자 키보드를 통한 입력
  IMAGE = 2;      // IMAGE Annotation를 통한 입력
  VIDEO = 3;      // VIDEO Annotation를 통한 입력
  SIGNAL = 100;   // 기타 장치에서 코드나 로직에 의해서
                  // 메시지를 전달하기 위한 입력
}
```

#### ResultCode enum
- 응답 코드

Range | Name | Value |Description
------|-----|-------|-----------
성공   | OK | 0, 기본값| 성공
시스템 오류| SYS_ERR | 11| 시스템 에러
&nbsp; | NET_ERR | 12| 네트워크 에러
입력    |MALFORMED_DATA |21 | input data format error
데이터  |INVALID_ARG |22|invalid argument
오류   |INVALID_USER |23 | user invalid
&nbsp; |INVALID_DEVICE | 24| 디바이스 데이터 오류
&nbsp; |INVALID_CL | 25 | invalid skill or intent
&nbsp; |INVALID_STATUS | 26|상태값 오류
각  |ERR_IN_CL | 31 | 분류기 오류
서브시스템  |ERR_IN_DA | 32 | 대화 에이전트 레벨 오류
단위  |ERR_IN_DM | 33 | LGE DM 오류
에러 |ERR_IN_SDS | 34 | 마인즈랩 SDS 오류
&nbsp; |ERR_IN_EB | 35| 마인즈랩 ExoBrain 오류
&nbsp; |ERR_IN_MRC | 36| 마인즈랩 MRC 오류
&nbsp; |ERR_IN_HPN | 37| 하이퍼넷 오류
&nbsp; |ERR_IN_BOT | 38| NMT 챗봇 오류
&nbsp; |ERR_IN_DB | 39| DB 오류
&nbsp; |ERR_IN_REST | 40| REST API 호출 오류
&nbsp; |ERR_IN_EX | 99| 외부 시스템 오류
프런트 서버 |USER_INVALIDATED | 101| 사용자 정보가 폐기되었음.
논리 오류  |SESSION_NOT_FOUND | 103 | 세션이 존재하지 않음(발생할 가능성 X)
&nbsp; | CLASSIFIER_FAILED | 301 | 도메인 분류 실패
&nbsp; | DA_NOT_FOUND |  302| 대화 에이전트가 없음.
&nbsp; | DA_INVALIDATED | 303 | 대화 에이전트 무효화
&nbsp; | LAST_DA_LOST | 304 | 마지막 대화에이전트가 사라짐.
&nbsp; | NO_MORE_CONTENT | 401 | PEEK_ANSWER의 경우,<br>추가적인 데이터가 없음.
&nbsp; | INTERNAL_ERROR | 500 | 내부 시스템 에러


```proto

// 에러 코드
// CL = classifer
// DA = dialog agent
// SYS = system
// NET = network
// DM = LGE dialog manager
// SDS = mindslab spoken dialog system
// EB = exobrain
// MRC = machine reading comprehention
// HPN = hyper net
// BOT = mindslab chatbot
// DB = database error
// EX = external system
enum ResultCode {
  OK = 0;

  SYS_ERR = 11;                     // 시스템 에러
  NET_ERR = 12;                     // 네트워크 에러
  
  // 입력 데이터 에러
  MALFORMED_DATA = 21;              // input data format error
  INVALID_ARG = 22;                 // invalid argument
  INVALID_USER =  23;               // user invalid
  INVALID_DEVICE = 24;              // 
  INVALID_CL = 25;                  // invalid skill or intent
  INVALID_STATUS = 26;              // 상태값 오류
  
  // 각 서브시스템 단위 에러
  ERR_IN_CL = 31;                   // DA 레벨 오류
  ERR_IN_DA = 32;                   // DA 레벨 오류
  ERR_IN_DM = 33;
  ERR_IN_SDS = 34;
  ERR_IN_EB = 35;
  ERR_IN_MRC = 36;
  ERR_IN_HPN = 37;
  ERR_IN_BOT = 38;
  ERR_IN_DB = 39;
  ERR_IN_EX = 99;

  USER_INVALIDATED = 101;           // 사용자 정보가 폐기되었음.
  SERVICE_GROUP_NOT_FOUND = 102;    // (쓰이지 않음) 서비스그룹 부정확
  SESSION_NOT_FOUND   = 103;        // 세션이 없습니다.
  SESSION_INVALIDATED = 104;        // 세션이 무효화된 상태.

  EMPTY_IN = 201;                   // 입력 텍스트가 비어있음.

  CLASSIFIER_FAILED = 301;          // 도메인 분류 실패
  DA_NOT_FOUND = 302;               // 대화 에이전트가 없음.
  DA_INVALIDATED = 303;             // 대화 에이전트 무효화
  LAST_DA_LOST = 304;               // 마지막 대화에이전트가 사라짐.
  CHATBOT_NOT_FOUND = 305;          // (NOT USED) 챗봇 없음.
  HUMAN_AGENT_NOT_FOUND = 306;      // (NOT USED) 인간 상담사 없음.
  SECONDARY_DIALOG_CONFLICT = 311;  // (NOT USED) (2차대화 충돌)
  LAST_DA_NOT_FOUND = 312;          // 지난 대화 에이전트 발견 되지 않음.
  DUPLICATED_SKILL_RESOLVED = 313;  // 도메인이 중복해서 조회됨.
  SECONDARY_DA_IS_MULTI_TURN = 314; // 2차 대화에서는 싱글턴만 가능함.

  NO_MORE_CONTENT = 401;            // PEEK_ANSWER의 경우,
                                    // 추가적인 데이터가 없음.

  INTERNAL_ERROR = 500;             // 내부 시스템 에러
}

enum LangCode {
  kor = 0;
  eng = 1;
}
```

#### UtterRequest 객체
- 대화 요청을 위한 객체

No.|Item|Type|Description|Default Value|Mandatory
---|----|----|-----------|-------------|---------
1  |utter | string | 텍스트 메시지| "" | M
2  |type | UtterInputType | 입력 유형 | SPEECH | M
3  |alt_utters | array of string | STT를 위한 추가적인 nbest utter <br>최대 길이는 제약은 없으나 통상 5개 이내 | Empty| O
4  |lang | LangCode| 언어 | kor | M
5  |meta | Struct| 추가적인 자체 포맷의 데이터 JSON | {} | O

```proto
// 발화 요청
message UtterRequest {
  string utter = 1;   // 텍스트 메시지
  UtterInputType type = 2; // 입력 유형
  repeated string alt_utters = 3; // 추가적인 nbest utter,
                                  // 최대 길이는 제약은 없으나 통상 5개 이내
  LangCode lang = 4;
  Struct meta = 5; // 추가적인 입력 메시지
}

```

#### UtterResponse 객체
- 대화 응답을 위한 객체
- 기존에 응답에 포함되었던 TTS를 위한 인코딩된 텍스트는 모두 meta 객체의 KEY-VALUE로
  이동한다.
- 예약된 meta key
  - selvas.tts
  - image.url

No.|Item|Type|Description|Default Value|Mandatory
---|----|----|-----------|-------------|---------
1  |utter | string | 기본 출력 텍스트 메시지| "" | M
2  |lang | LangCode| 언어 | kor | M
3  |meta | Struct | 추가적인 출력 메시지 <br> 예약된 meta key: <br>"selvas.tts"<br> "image.url" | null | O


```proto
// 발화 응답
message UtterResponse {
  string utter = 1;   // 기본 텍스트 메시지
  LangCode lang = 2;
  Struct meta = 3; // 추가적인 출력 메시지
        // "selvas.tts"
        // "image.url"
}
```

#### UtterResponse 객체
일반적인 JSON 객체를 나타낸다. 기본적으로 Object 형태이거나, Object의 배열을 포함하고
내부적으로 복잡한 계층을 가져도 아무런 문제가 없다.


```proto

// The JSON representation for `Struct` is JSON object.
message Struct {
  map<string, Value> fields = 1;
}

message Value {
  // The kind of value.
  oneof kind {
    // Represents a null value.
    NullValue null_value = 1;
    // Represents a double value.
    double number_value = 2;
    // Represents a string value.
    string string_value = 3;
    // Represents a boolean value.
    bool bool_value = 4;
    // Represents a structured value.
    Struct struct_value = 5;
    // Represents a repeated `Value`.
    ListValue list_value = 6;
  }
}

//  The JSON representation for `NullValue` is JSON `null`.
enum NullValue {
  // Null value.
  NULL_VALUE = 0;
}

// The JSON representation for `ListValue` is JSON array.
message ListValue {
  // Repeated field of dynamically typed values.
  repeated Value values = 1;
}

```

## FRONT REST API

### /analyze
- 목적 및 기능
  - 대화 의도 분류
  - 대화 응답 생성
- URL: $prefix/analyze
- Request HEADERS:
  - X-nlp-session-id: `[0-9]*`
    - X-nlp-session-id는 마지막 X-nlp-session-id를 전달한다. 없으면 보내주지 않는다.
    - 요청한 X-nlp-session-id가 만료된 경우에는 응답 X-nlp-session-id가 바뀌어서 전달 될 수 있다.
    - X-nlp-session-id는 analyze에서만 변경될 수 있다.
- Response HEADERS
  - "X-nlp-session-id: `[0-9]*`
    - 항상 내려간다.
  - "X-nlp-session-reset": true
    - 새로 만들어지거나 변경되었을 경우에만 전송
- Request
  - TalkQuery { }
  - 매 호출 시마다, `tpo_context`와 `device` 정보를 보낼 필요가 없다.
  - 세션을 오픈할 때는 반드시 보내야 한다. `X-nlp-session-id`가 없는 경우
  - 세션이 무효화되어 있는 경우, `tpo_context`와 `device` 정보가 없으면 에러 메지시를
    내보낸다. 다시 채워서 보내주면 된다. 10분 또는 5분 이상 입력이 없으면 장치에서 충분히
    제어 가능하다.
  - svc_group은 명시적으로 입력되어야 하며, 없을 경우("")는 설정으로 부터 읽어오도록 처리한다.
- Response:
  - TalkAnalysis { }

#### TalkQuery
- 입력 

No.|Item|Type|Description|Default Value|Mandatory
---|----|----|-----------|-------------|---------
1  |query | UtterRequest | 요청 메시지 | - | M
2  |svc_group | string | 서비스 그룹 | "" | M
3  |tpo_context | TpoContext| TPO Context| null | O
4  |device | Device | Device 정보| null | O

```proto
message TalkQuery {
  UtterRequest query = 1;    // 요청 메시지
  string svc_group = 2;
  TpoContext tpo_context = 11; // TPO Context
  Device device = 12;  // Device 정보
}

```

#### TalkAnalysis

No.|Item|Type|Description|Default Value|Mandatory
---|----|----|-----------|-------------|---------
1  |res_code | ResultCode | 응답 코드  | "OK" | M
2  |error_message | string| 에러가 있을 경우에만 상세한 에러 메시지| "" | O
3  |skill | string | SKILL | "" | M
4  |intent| string | INTENT | "" | O
5  |is_answer | bool| 응답일 경우 true| false | M
6  |has_more_answer | bool| 추가적인 답변이 가능한 경우 true | false | M
7  |has_slots | bool| 슬롯 정보가 있을 경우 true| false | M
8  |answer | UtterResponse | 대화 응답 | {} | O
9  |filled_slots | Key Value Object | 채워진 슬롯의 이름과 값 | {} | O
10 |empty_slots | array of string| 빈 슬롯의 이름 | {} |  O


```proto
// 대화에 대한 이해의 결과를 반환한다.
message TalkAnalysis {
  ResultCode res_code = 1;
  string error_message = 2;

  string skill = 11;
  string intent = 12;

  bool is_answer = 21;
  bool has_more_answer = 22;
  bool has_slots = 23;
  // is_final이면 UtterResponse가 존재함.
  UtterResponse answer = 101;

  // is_final이 아니고 has_slots이면 Slot 정보가 필요함.
  map<string, string> filled_slots = 201;
  repeated string empty_slots = 202;
}

```

#### Example for analyze with answer
```
// 최초 X-nlp-session-id를 발급 
POST /analyze
{
  "query": {
    "utter" : 오늘 날씨 어때?",
    "type" : "KBD",
    "alt_utters" : [
      "오늘 날씨 괜찮아?",
      "오늘 날씨 흐려?",
      "오늘 날씨 밖에 나가기 좋아?"
    ]
    "lang" : "kor",
    "meta" : {
      "k1" : "v1",
      "k2" : "v2",
      "k3" : "v3",
      "k4" : "v4",
    }
  }
  "tpo_context": {
    "time": "오늘",
    "place": "미쿡",
    "user_key": "u00001"
    "meta": {
      "k1": "v5",
      "k2": "v6",
      "k3": "v7",
      "k4": "v8"
    }
  },
  "device": {
    "type": "connected-car",
    "model": "MODEL100101",
    "no": "3940329402394",
    "timestamp": {
      "seconds": 1495160754,
      "nanos": 0
    }
    "meta": {
    }
  }
}

200 OK
X-nlp-session-id : 12121212
X-nlp-session-reset : true
{
  "res_code": "OK",
  "error_message": "",
  "skill": "WEATHER",
  "intent": "WEATHER>LOCATION",
  "is_answer": true,
  "has_more_answer": false,
  "has_slots": true,
  "answer": {
    "utter": "지역을 말씀해주세요",
    "lang" : "kor",
    "meta": {
      "k1": "v1",
      "k2": "v2",
      "k3": "v3",
      "k4": "v4"
    }
  },
  "filled_slots": null,
  "empty_slots": null
}

// 만료된 X-nlp-session-id를 재발급
POST /analyze
X-nlp-session-id: 12121212
{
  "query": {
    "utter" : 오늘 날씨 어때?",
    "type" : "KBD",
    "alt_utters" : [
      "오늘 날씨 괜찮아?",
      "오늘 날씨 흐려?",
      "오늘 날씨 밖에 나가기 좋아?"
    ]
    "lang" : "kor",
    "meta": {
      "k1" : "v1",
      "k2" : "v2",
      "k3" : "v3",
      "k4" : "v4",
    }
  }
  "tpo_context": {
    "time": "오늘",
    "place": "미쿡",
    "user_key": "u00001"
    "ext_contexts": {
      "k1": "v5",
      "k2": "v6",
      "k3": "v7",
      "k4": "v8"
    }
  },
  "device": {
    "type": "connected-car",
    "model": "MODEL100101",
    "no": "3940329402394",
    "timestamp": {
      "seconds": 1495160754,
      "nanos": 0
    }
    "meta": {
    }
  }
}

200 OK
X-nlp-session-id : 34343434
X-nlp-session-reset : true
{
  "res_code": "OK",
  "error_message": "",
  "skill": "WEATHER",
  "intent": "WEATHER>LOCATION",
  "is_answer": true,
  "has_more_answer": false,
  "has_slots": true,
  "answer": {
    "utter": "지역을 말씀해주세요",
    "lang" : "kor",
    "meta": {
      "k1": "v1",
      "k2": "v2",
      "k3": "v3",
      "k4": "v4"
    }
  },
  "filled_slots": {
    "time": "오늘",
  },
  empty_slots: [
    "area",
    "lareaNm",
    "mareaNm",
    "sareaNm"
  ]
}

// 현재 유지중인 X-nlp-session-id
POST /analyze
X-nlp-session-id: 12121212
{
  "query": {
    "utter" : 오늘 날씨 어때?",
    "type" : "KBD",
    "alt_utters" : [
      "오늘 날씨 괜찮아?",
      "오늘 날씨 흐려?",
      "오늘 날씨 밖에 나가기 좋아?"
    ]
    "lang" : "kor",
    "meta": {
      "k1" : "v1",
      "k2" : "v2",
      "k3" : "v3",
      "k4" : "v4",
    }
  }
}

200 OK
X-nlp-session-id : 12121212
{
  "res_code": "OK",
  "error_message": "",
  "skill": "WEATHER",
  "intent": "WEATHER>LOCATION",
  "is_answer": true,
  "has_more_answer": false,
  "has_slots": true,
  "answer": {
    "utter": "지역을 말씀해주세요",
    "lang" : "kor",
    "meta": {
      "k1": "v1",
      "k2": "v2",
      "k3": "v3",
      "k4": "v4"
    }
  },
  "filled_slots": {
    "time": "오늘",
  },
  empty_slots: [
    "area",
    "lareaNm",
    "mareaNm",
    "sareaNm"
  ]
}

// SIGNAL type
POST /analyze
X-nlp-session-id: 12121212
{
  "query": {
    "utter" : 안녕하세요?",
    "type" : "SIGNAL",
    "alt_utters" : "",
    "lang" : "kor",
    "meta": {
      "k1" : "v1",
      "k2" : "v2",
      "k3" : "v3",
      "k4" : "v4",
    }
  }
  "tpo_context": {
    "time": "오늘",
    "place": "미쿡",
    "user_key": "u00001"
    "ext_contexts": {
      "k1": "v5",
      "k2": "v6",
      "k3": "v7",
      "k4": "v8"
    }
  },
  "device": {
    "type": "connected-car",
    "model": "MODEL100101",
    "no": "3940329402394",
    "timestamp": {
      "seconds": 1495160754,
      "nanos": 0
    }
    "meta": {
    }
  }
}

200 OK
X-nlp-session-id: 12121212
{
  "res_code": "OK",
  "error_message": "",
  "skill": "",
  "intent": "",
  "is_answer": true,
  "has_more_answer": false,
  "has_slots": true,
  "answer": {
    "utter": "오늘은 조금 늦으셨네요",
    "lang" : "kor",
    "meta": {
      "selvas.tts" : "<p>오늘</p>은+조금+늦으셨네요",
    }
  },
  "filled_slots": null,
  "empty_slots" : null
}

// X-nlp-session-id가 무효화되고, tpo_context, device가 없을 경우
POST /analyze
X-nlp-session-id: 12121212
{
  "query": {
    "utter" : 오늘 날씨 어때?",
    "type" : "KBD",
    "alt_utters" : [
      "오늘 날씨 괜찮아?",
      "오늘 날씨 흐려?",
      "오늘 날씨 밖에 나가기 좋아?"
    ]
    "lang" : "kor",
    "meta": {
      "k1" : "v1",
      "k2" : "v2",
      "k3" : "v3",
      "k4" : "v4",
    }
  }
}

200 OK
X-nlp-session-id : 34343434
X-nlp-session-reset : true
{
  "res_code": "SESSION_NOT_FOUND",
  "error_message": "세션이 만료되었습니다.",
  "skill": "",
  "intent": "",
  "is_answer": false,
  "has_more_answer": false,
  "has_slots": false,
  "answer": {
  },
  "filled_slots": null,
  "empty_slots" : null
}

POST /analyze
X-nlp-session-id: 34343434
{
  "query": {
    "utter" : 오늘 날씨 어때?",
    "type" : "KBD",
    "alt_utters" : [
      "오늘 날씨 괜찮아?",
      "오늘 날씨 흐려?",
      "오늘 날씨 밖에 나가기 좋아?"
    ]
    "lang" : "kor",
    "meta": {
      "k1" : "v1",
      "k2" : "v2",
      "k3" : "v3",
      "k4" : "v4",
    }
  }
  "tpo_context": {
    "time": "오늘",
    "place": "미쿡",
    "user_key": "u00001"
    "ext_contexts": {
      "k1": "v5",
      "k2": "v6",
      "k3": "v7",
      "k4": "v8"
    }
  },
  "device": {
    "type": "connected-car",
    "model": "MODEL100101",
    "no": "3940329402394",
    "timestamp": {
      "seconds": 1495160754,
      "nanos": 0
    }
    "meta": {
    }
  }
}

200 OK
X-nlp-session-id : 34343434
{
  "res_code": "OK",
  "error_message": "",
  "skill": "WEATHER",
  "intent": "WEATHER>LOCATION",
  "is_answer": true,
  "has_more_answer": false,
  "has_slots": true,
  "answer": {
    "utter": "지역을 말씀해주세요",
    "lang" : "kor",
    "meta": {
      "k1": "v1",
      "k2": "v2",
      "k3": "v3",
      "k4": "v4"
    }
  },
  "filled_slots": {
    "time": "오늘",
  },
  empty_slots: [
    "area",
    "lareaNm",
    "mareaNm",
    "sareaNm"
  ]
}
```

#### Example for analyze with fill slots
```
POST /analyze
X-nlp-session-id: 12121212

{
  "query": {
    "utter" : "판교,"
    "type" : "KBD",
    "alt_utters" : [
    ]
    "lang" : "kor",
    "meta" : {
    }
  }
  "tpo_context": {
    "time": "오늘",
    "place": "미쿡",
    "user_key": "u00001"
    "ext_contexts": {
      "k1": "v5",
      "k2": "v6",
      "k3": "v7",
      "k4": "v8"
    }
  },
  "device": {
    "type": "connected-car",
    "model": "MODEL100101",
    "no": "3940329402394",
    "timestamp": {
      "seconds": 1495160754,
      "nanos": 0
    }
    "meta": {
    }
  }
}

200 OK
X-nlp-session-id : 12121212
{
  "res_code": "OK",
  "error_message": "",
  "skill": "WEATHER",
  "intent": "WEATHER>TIME",
  "is_answer": false,
  "has_more_answer": false,
  "has_slots": true,
  "answer": {},
  "filled_slots": {
    "time": "오늘",
    "area": "판교",
    "lareaNm" : "경기도",
    "mareaNm" : "성남시 분당구",
    "sareaNm" : "판교"
  },
  empty_slots: [
    "humidity",
    "maxTemp",
    "minTemp"
  ]
}

```

### /make-answer
- 목적 및 기능
  - 대화 응답 생성
- URL: $prefix/make-answer/:skill
- Request HEADERS:
  - X-nlp-session-id: `[0-9]*`
    - 필수
- Response HEADERS
  - "X-nlp-session-id: `[0-9]*`
    - 항상 내려간다.
- Request
  - AnswerSlot { }
- Response:
  - Answer { }

#### AnswerSlot

No.|Item|Type|Description|Default Value|Mandatory
---|----|----|-----------|-------------|---------
1  |skill | string | SKILL | "" | M
2  |intent| string | INTENT | "" | O
3  |slots | Key Value Object | 채워진 슬롯 정보| {} | O
4  |data | Struct | 추가적인 자체 포맷의 데이터 JSON | {}| O

```proto
message AnswerSlot {
  string skill = 1;
  string intent = 2;

  map<string, string> slots = 11;
  Struct data = 21;
}
```

#### Answer

No.|Item|Type|Description|Default Value|Mandatory
---|----|----|-----------|-------------|---------
1  |res_code | ResultCode | 응답 코드  | "OK" | M
2  |error_message | string| 에러가 있을 경우에만 상세한 에러 메시지| "" | O
3  |skill | string | SKILL | "" | M
4  |intent| string | INTENT | "" | O
5  |has_more_answer | bool| Device 정보| false | M
6  |answer | UtterResponse | 대화 응답 | {} | M

```proto
message Answer {
  ResultCode res_code = 1;
  string error_message = 2;

  string skill = 11;
  string intent = 12;

  bool has_more_answer = 21;
  UtterResponse answer = 101;
}
```
#### Example for make-answer
```
POST /make-answer/WEATHER
X-nlp-session-id: 12121212
{
  "skill": "WEATHER",
  "intent": "WEATHER>SUB",
  "slots": {
    "time": "오늘",
    "area" : "판교",
    "humidity" : "맑음",
    "maxTemp" : "11.0",
    "minTemp" : "3.0"
  },
  "data" : {
    "weatherData" : [
      {
        "data1": "value1"
      },
      {
        "data2": "value2"
      },
      {
        "data3": "value3"
      },
      {
        "data4": "value4"
      }
    ]
  }
}

200 OK
X-nlp-session-id: 12121212
{
  "res_code": "OK",
  "error_message": "",
  "skill": "WEATHER",
  "intent": "WEATHER>CURRENT",
  "has_more_answer": false,
  "answer": {
    "utter": "오늘 판교 날씨는 흐리고 기온은 3도에서 11도까지입니다.",
    "lang" : "kor",
    "meta": {
      "k1": "v1",
      "k2": "v2",
      "k3": "v3",
      "k4": "v4"
    }
  }
}
```

### /peek-answer
- URL: $prefix/peek-answer
- METHOD: GET
- Request HEADERS:
  - X-nlp-session-id: `[0-9]*`
    - 필수
- Response HEADERS
  - "X-nlp-session-id: `[0-9]*`
    - 항상 내려간다.
- Request
- Response:
  - Answer { }

#### Example for peek-answer
```
GET /peek-answer
X-nlp-session-id: 12121212
{
}

200 OK
X-nlp-session-id: 12121212
{
  "res_code": "OK",
  "error_message": "",
  "skill": "WEATHER",
  "intent": "WEATHER>CURRENT",
  "has_more_answer": false,
  "answer": {
    "utter": "근데 내일부터 13호 태풍이 남해안에 상륙한다는데 자세한 정보 알려드릴까요.",
    "lang" : "kor",
    "meta": {
      "k1": "v1",
      "k2": "v2",
      "k3": "v3",
      "k4": "v4"
    }
  }
}
```

## LGE NLP와 FRONT 서버간의 연동 규격
- LGE의 검토 결과에 따르지만, 위의 `/analyze`와 `/make-answer`를 기준으로 호출하기를 권장한다.
  - 추가적으로 필요한 통신을 위해서 정의되어야할 사항이 있으면
    `TalkQuery`, `TalkAnalysis`, `Answer`를 확장하는 방식으로
    접근하도록 한다.
- 기존의 대화 및 신규 대화에 대해서 모든 처리가 가능해야 한다.

### 기존 공통 메시지

```proto

enum NlpResultCode {
  NLPUNKNOWN = 0;
  NLP00001 = 1;
  NLP00002 = 2;
  NLP00003 = 3;
  NLP00004 = 4;
  NLP00005 = 5;
  NLP00006 = 6;
  NLP00007 = 7;
  NLP00008 = 8;
  NLP00011 = 11;
  NLP00012 = 12;
  NLP00013 = 13;
  NLP00014 = 14;
  NLP00015 = 15;
  NLP00016 = 16;
  NLP00017 = 17;
  NLP00018 = 18;
  NLP00019 = 19;
  NLP00020 = 20;
  NLP00021 = 21;
  NLP00022 = 22;
  NLP00023 = 23;
  NLP00024 = 24;
  NLP00025 = 25;
  NLP00026 = 26;
  NLP00027 = 27;
  NLP00028 = 28;
  NLP01000 = 1000;
  NLP01001 = 1001;
  NLP01002 = 1002;
  NLP01003 = 1003;
  NLP10001 = 10001;
  NLP10002 = 10002;
  NLP10003 = 10003;
  NLP11001 = 11001;
  NLP11002 = 11002;
  NLP11003 = 11003;
  NLP12001 = 12001;
  NLP12002 = 12002;
  NLP12003 = 12003;
  NLP13001 = 13001;
  NLP14001 = 14001;
  NLP15001 = 15001;
  NLP16001 = 16001;
  NLP17001 = 17001;
  NLP19001 = 19001;
  NLP99001 = 99001;
  NLP99002 = 99002;
  NLP99003 = 99003;
  NLP99004 = 99004;
}

enum Function {
  FUNC_UNKNOWN = 0;
  FUNC_ANALYSIS = 1;
  FUNC_MAKE_ANSWER = 2;
  FUNC_COMMON = 3
  FUNC_INITIALIZE = 4;
  FUNC_CONTEXT_RESET = 5;
  FUNC_YN = 6
}

enum ResultType {
  RES_UNKNOWN = 0;
  RES_ANALYSIS = 1;
  RES_ANALYSIS_ANSWER = 2;
  RES_ANSWER = 3;
  RES_ANSWER_CONTINUE = 4;
  RES_ANSWER_YES = 5;
  RES_ANSWER_NO = 6;
  RES_COMMON = 7;
}

message NlpRequest {
  Function function = 1;
  string deviceType = 2;
  string deviceModel = 3;
  string deviceNo = 4;
  string deviceTime = 5;
  string sessionId = 6;
  string songId = 7;
  string trxId = 8;
  string query = 9;
  string location = 10;
  string serviceDomain = 11;
  string serviceAct = 12;
  string statusId = 13;
  string serviceResultCode = 14;
  Struct data = 15;
}

message NlpResponse {
  ResultCode resultCode = 1;
  ResultType resultType = 2;
  string utter = 3;
  string utter_enc = 4;
  string url = 5;
  string imageUrl = 6;
  string serviceDomain = 7;
  string serviceAct = 8;
  string statusId = 9;
  Struct data = 15;
}

```
