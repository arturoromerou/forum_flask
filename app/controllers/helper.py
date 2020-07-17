def date_format(value):
    months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre",
        "Octubre", "Noviembre", "Diciembre")
    month = months[value.month - 1]
    return f"{value.day} de {month} del {value.year}"