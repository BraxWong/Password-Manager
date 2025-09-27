def search_website(website_list,user_input):
    user_input = user_input.lower().strip()
    scores = [] 
    for website in website_list:
        website = website.website_name.lower().split()
        current_website_score = 0
        user_input_iter = 0
        for w in website:
            word_score = 0
            for letter in w:
                if user_input_iter == len(user_input):
                    continue
                if letter == user_input[user_input_iter]:
                    word_score +=1 
                    user_input_iter+=1
                else:
                    user_input_iter=0
            current_website_score = max(current_website_score,word_score)
        scores.append(current_website_score) 
    return scores
