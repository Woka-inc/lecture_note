# 필요한 라이브러리 import
from langchain_openai import ChatOpenAI  # OpenAI의 ChatGPT API와 연결하기 위한 라이브러리
from langchain_experimental.agents import create_pandas_dataframe_agent  # Pandas DataFrame을 처리하기 위한 LangChain agent
import os  # 운영체제와 상호작용을 위한 라이브러리

# Model 클래스 정의
class Model:
    def __init__(self, data):
        # 환경 변수로 OpenAI API 키 설정 (API 키는 개인 정보이므로 안전하게 관리해야 합니다)
        os.environ["OPENAI_API_KEY"] = 'YOUR OPENAI API KEY'
        
        # Pandas DataFrame을 처리하는 OpenAI 에이전트를 생성
        self.agent = create_pandas_dataframe_agent(
            ChatOpenAI(model="gpt-4o-mini", temperature=0),  # GPT-4 모델을 사용, 온도는 0으로 설정하여 예측을 결정적으로 만듦
            data,  # 데이터는 Pandas DataFrame 형식으로 전달
            verbose=True,  # 디버깅 정보를 출력 (과정에서 발생하는 정보를 자세히 볼 수 있음)
            agent_type='openai-tools',  # 에이전트 유형을 지정
            allow_dangerous_code=True,  # 위험한 코드를 실행할 수 있도록 허용 (신중하게 사용해야 함)
            max_iterations=10  # 최대 10번의 반복을 허용
        )
    
    # 주식 데이터에 대한 통찰을 얻기 위한 메서드
    def get_insight(self):
        # 에이전트를 호출하여 명령을 전달
        result = self.agent.invoke("""
            1. 최근 3년 데이터를 살펴보고 buy, hold, sell 중 어떤 action을 해야할지 신중하게 생각하고 알려줘
            2. Action: [Buy] 형식으로 알려줘
            3. 알려준 action을 선택한 이유 3가지를 주식 트레이딩 전문가에게 설명하듯 자세히 알려줘
            4. 3번에서 알려준 내용을 초등학생도 쉽게 이해할 수 있도록 3줄 이내로 요약해서 알려줘
            5. 요약은 '간단 요약' 타이틀을 사용해
            6. 3과 4를 비교해보고 의미가 일치하는지 검증해. 일치하지 않으면 3의 내용에 맞춰 4의 내용을 수정해                                   
            7. 한글로 알려줘
            8. 기술적인 지표를 사용하여 설명할 땐 값을 명시하면서 설명해
            9. 아래의 양식에 따라 작성해. 절대 양식을 벗어나지마.
            **Action:** Buy       
            **Insight:**
                - say something
                - say something
                - say something
                - say something
            **Summary:**
                - say something
                - say something
                - say something
            10. 만약 Action이 Buy였다면 언제 sell을 하면 좋을지를 추천하고 근거를 알려줘
        """)
        # 결과를 반환 (결과는 JSON 형식으로 포함된 데이터)
        return result["output"]