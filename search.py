# Searching element from database "DB.txt"
def search_in_file(text_form_user):
    sorted_db = []
    count = 0
    try:
        file_db = open('DB.txt')
        for line in file_db:
            line = line[2:-3].split("', '")
            value = line[1].lower()
            search_response = value.find(text_form_user.lower())
            if search_response != -1:
                sorted_db.append(line)
                count = count + 1
            # Limiting the number of search records
            if count == 20:
                break
        return sorted_db, count
    except IOError:
        return print('[INFO] Error opening DB')
