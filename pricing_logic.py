import math

def calculate_program_cost(prog, students, section_size, max_sections_per_teacher, discount_percent, school_days):
    sections = math.ceil(students / section_size)

    if sections < 20:
        full_teachers = 0
        teacher_days = math.ceil(sections / 5)
        teacher_day_cost = teacher_days * 2000 * 35
    else:
        full_teachers = sections // max_sections_per_teacher
        remaining = sections % max_sections_per_teacher
        if 0 < remaining < 20:
            teacher_days = math.ceil(remaining / 5)
            teacher_day_cost = teacher_days * 2000 * 35
        elif remaining >= 20:
            full_teachers += 1
            teacher_days = 0
            teacher_day_cost = 0
        else:
            teacher_days = 0
            teacher_day_cost = 0

    teacher_cost = 425000 if prog == "STEM" else 400000
    teacher_cost_total = full_teachers * teacher_cost
    book_cost = students * 200
    kit_cost = 115000 if prog == "STEM" else 0
    manager_cost = 50000

    program_cost = teacher_cost_total + teacher_day_cost + book_cost + kit_cost
    total_program_cost = program_cost + manager_cost

    base_price = total_program_cost / (1 - 0.4)
    final_price = base_price * (1 - discount_percent / 100)
    gross_margin = 100 - ((total_program_cost / final_price) * 100)

    if gross_margin < 30:
        return None, gross_margin

    price_per_student = final_price / students
    book = min(price_per_student, 1800 if prog == "STEM" else 1200)
    service = max(price_per_student - book, 0)
    gst = round(service * 0.18) if service > 0 else 0

    result = {
        "final_price": final_price,
        "price_per_student": price_per_student,
        "book": book,
        "service": service,
        "gst": gst,
        "students": students,
        "teacher_days": teacher_days,
        "full_teachers": full_teachers,
        "gross_margin": gross_margin
    }
    return result, gross_margin
