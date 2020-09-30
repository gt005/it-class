function getCorrectNameForPoints (number) {
    if ((10 <= number % 100) && (number % 100 <= 20) || (number % 10 == 0) || (5 <= (number % 10)) && ((number % 10) <= 9)) {
        return "Баллов"
    } else if (number % 10 == 1) {
        return "Балл"
    }
    return "Балла"
}
