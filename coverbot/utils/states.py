from aiogram.dispatcher.filters.state import StatesGroup, State


class Main(StatesGroup):
    main_menu = State()
    settings = State()
    history = State()


class Settings(StatesGroup):
    enter_user_name = State()
    enter_years_of_experience = State()
    enter_last_position = State()
    enter_skills = State()
    enter_sphere_of_work = State()
