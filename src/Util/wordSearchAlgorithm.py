def searchWebsite(websiteList,userInput):
    userInput = userInput.lower().strip()
    scores = [] 
    for website in websiteList:
        website = website.lower().split()
        currentWebsiteScore = 0
        userInputIter = 0
        for w in website:
            wordScore = 0
            for letter in w:
                if userInputIter == len(userInput):
                    continue
                if letter == userInput[userInputIter]:
                    wordScore +=1 
                    userInputIter+=1
                else:
                    userInputIter=0
            currentWebsiteScore = max(currentWebsiteScore,wordScore)
        scores.append(currentWebsiteScore) 
    return scores