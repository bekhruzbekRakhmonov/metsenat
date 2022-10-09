from django import template

register = template.Library()

@register.filter(name="range_pages")
def range_pages(value):
    try:
        value = int(value)
        l = [i for i in range(1,value+1)]
        return l
    except TypeError:
        return value

@register.filter(name="parse_money")
def parse_money(summa):
    try:
        summa = str(int(summa))
        parsed_summa = ""
        c = 0
        for i in range(len(summa)-1,-1,-1):
            if c == 3:
                parsed_summa = " " + parsed_summa
                c = 0
            parsed_summa = summa[i] + parsed_summa
            c += 1

        return parsed_summa
    except Exception:
        return 0

@register.filter(name="parse_phone")
def parse_phone(phone):
    pass