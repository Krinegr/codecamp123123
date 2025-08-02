from BD.models import Support
from engine import EngineController

class SupportRepository:
    database_controler = EngineController()

    @classmethod
    def create_question(cls, telegram_id: str, username: str, question: str) -> None:
        session = cls.database_controler.create_session()
        support = Support(
            telegram_id=telegram_id,
            username=username,
            question=question
        )
        session.add(support)
        session.commit()
        session.close()
    
    @classmethod
    def get_question(cls) -> Support:
        session = cls.database_controler.create_session()
        question = session.query(Support).first()
        session.close()
        return question
    
    @classmethod
    def get_all_questions(cls) -> list[Support]:
        session = cls.database_controler.create_session()
        questions = session.query(Support).all()
        session.close()
        return questions

    @classmethod
    def delete_question(cls, telegram_id: str) -> None:
        session = cls.database_controler.create_session()
        support = session.query(Support).filter(
            Support.telegram_id == telegram_id
        ).first()
        session.delete(support)
        session.commit()
        session.close()
