def searchWebsite(websiteList,userInput):
    userInput = userInput.lower()
    scores = [] 
    for website in websiteList:
        website = website.lower()
        currentWebsiteScore = 0
        userInputIter = 0
        for letter in website:
            if letter == userInput[userInputIter]:
                currentWebsiteScore +=1 
                userInputIter+=1
            else:
                userInputIter=0
        scores.append(currentWebsiteScore) 
    return scores