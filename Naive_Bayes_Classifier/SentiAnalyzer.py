import math

class SentiAnalyzer:

    # Make the method signature to accept "sentidata" and "word"
    def __init__(self):
        print('This is a senti analyzer')
    
    def probWordPositiveAndNegative(self, sentidata, word, idxWord):
        """
        각 단어에 대한 조건부 확률을 구하는 함수
        word에서 인덱스가 idxWord인 단어가
        각 리뷰 데이터에 발생하는지,
        즉 해당 단어가 얼마나 positive한 지를 계산
        """
        pointedWord = word[idxWord]
        reviews = [int(float(row[-1])) for row in sentidata]
        occurrence = [int(float(row[idxWord])) for row in sentidata]
        
        # Calculate the number of positive review occurrence with the pointed word, and assign the calculated value to 'positive'
        positive = 0
        for i in range(len(occurrence)):
            positive = positive + (occurrence[i] and reviews[i])

        # Calculate the number of positive reviews from the entire review set
        numPositiveReviews = reviews.count(1)

        # Calculate the number of negative review occurrence with the pointed word, and assign the calculated value to 'negative'
        negative = 0
        for i in range(len(occurrence)):
            negative = negative + (occurrence[i] == 1 and reviews[i] == 0)

        rowCount = len(sentidata)
        
        positiveProb = float(positive) / float(numPositiveReviews)
        negativeProb = float(negative) / float(rowCount - numPositiveReviews)
        
        if positiveProb == 0:
            positiveProb = 0.00001
        if negativeProb == 0:
            negativeProb = 0.00001
        return pointedWord, positiveProb, negativeProb

    def probPositiveAndNegative(self, sentidata):
        """
        사전 확률을 구하는 부분이다.
        전체 리뷰 개수에서 Positive와 Negative에 속하는
        리뷰의 비율을 반환.
        """
        positive = sum([int(float(row[-1])) for row in sentidata])
        numReviews = len(sentidata)
        negative = numReviews - positive
        positiveProb = float(positive) / float(numReviews)
        negativeProb = float(negative) / float(numReviews)
        return positiveProb, negativeProb

    def findUsedWords(self, sentidata, word, idx):
        """
        각 문서마다 사용된 단어를 뽑아내는 함수
        """
        # Return the index of the used words in 'idx'th review
        temp = [int(float(x)) for x in sentidata[idx][:-1]]
        idxUsedWords = [index for index, value in enumerate(temp) if value == 1]
        # Return the actual words in 'idx'th review
        usedWords = [word[idx] for idx in idxUsedWords]
        return idxUsedWords, usedWords

    def runAnalysis(self, sentidata, word, idxReview):
        """
        실제 분석을 실행하는 함수
        """
        probLogPositive = 0
        probLogNegative = 0
        idxUsedWords, usedWords = self.findUsedWords(sentidata, word, idxReview)

        # Make a for-loop to run from the first word to the last word
        for i in range(len(idxUsedWords)):
            # get the first word from the used word set
            idxWord = idxUsedWords[i]
            # calculate the word's probability to be positive or negative
            pointedWord, positive, negative = self.probWordPositiveAndNegative(sentidata, word, idxWord)
            probLogPositive += math.log(positive)
            probLogNegative += math.log(negative)

        #multiply priority probability
        positiveProb1, negativeProb1 = self.probPositiveAndNegative(sentidata)
        probLogPositive += math.log(positiveProb1)
        probLogNegative += math.log(negativeProb1)

        if probLogPositive > probLogNegative:
            sentiment = 'Positive'
            print('Positive')
        else:
            sentiment = 'Negative'
            print('Negative')

        return probLogPositive, probLogNegative, sentiment

