from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import os 

class Model:
    def __init__(self, data):
        os.environ["OPENAI_API_KEY"] = 'YOUR OPENAI API KEY'
        self.agent = create_pandas_dataframe_agent(
            ChatOpenAI(model="gpt-4o-mini", temperature=0),
            data,
            verbose=True,
            agent_type='openai-tools',
            allow_dangerous_code=True,
            max_iterations=10
            )
        
    def get_insight(self):
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
            **Inshgit:**
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
        return result["output"]