from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import getallcategory,getcategoryplaces
def vote():
    vote_markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="ovoz berish 📣",callback_data="vote")
    vote_markup.add(button)
    return vote_markup


def categories():
    category = InlineKeyboardMarkup(row_width=2)
    for i in getallcategory():
        category.row(
            InlineKeyboardButton(text=f"{i.get('name')}", callback_data=f"forallcategory{i.get('name')}")
        )
    return category

def categoryplaces(category_name):
    place = InlineKeyboardMarkup(row_width=3)
    for i in getcategoryplaces(category_name):
        place.row(
                 InlineKeyboardButton(text=f"{i.get('name')}", callback_data=f"forplaces{i.get('name')}")
                  )
    return place
