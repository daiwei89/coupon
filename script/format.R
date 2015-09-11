### Kaggle Scripts: Ponpare Coupon Purchase Prediction ###
### Author: Subhajit Mandal ###

#read in all the input data
cpdtr <- read.csv("../data/coupon_detail_train.csv")
cpltr <- read.csv("../data/coupon_list_train.csv")
cplte <- read.csv("../data/coupon_list_test.csv")
ulist <- read.csv("../data/user_list.csv")

#making of the train set
cpltr$USER_ID_hash <- "realuser"
train <- cpltr
train <- train[,c("USER_ID_hash","COUPON_ID_hash",
                  "GENRE_NAME","DISCOUNT_PRICE","PRICE_RATE",
                  "USABLE_DATE_MON","USABLE_DATE_TUE","USABLE_DATE_WED","USABLE_DATE_THU",
                  "USABLE_DATE_FRI","USABLE_DATE_SAT","USABLE_DATE_SUN","USABLE_DATE_HOLIDAY",
                  "USABLE_DATE_BEFORE_HOLIDAY","large_area_name","ken_name","small_area_name")]
#combine the test set with the train
cplte$USER_ID_hash <- "dummyuser"
cplte$ITEM_COUNT <- 0

cpchar <- cplte[,c("USER_ID_hash","COUPON_ID_hash",
                   "GENRE_NAME","DISCOUNT_PRICE","PRICE_RATE",
                   "USABLE_DATE_MON","USABLE_DATE_TUE","USABLE_DATE_WED","USABLE_DATE_THU",
                   "USABLE_DATE_FRI","USABLE_DATE_SAT","USABLE_DATE_SUN","USABLE_DATE_HOLIDAY",
                   "USABLE_DATE_BEFORE_HOLIDAY","large_area_name","ken_name","small_area_name")]

train <- rbind(train,cpchar)
#NA imputation
train[is.na(train)] <- 1
#convert the factors to columns of 0's and 1's
train <- cbind(train[,c(1,2)],model.matrix(~ -1 + .,train[,-c(1,2)],
                                           contrasts.arg=lapply(train[,names(which(sapply(train[,-c(1,2)], is.factor)==TRUE))], contrasts, contrasts=FALSE)))

#separate the test from train
test <- train[train$USER_ID_hash=="dummyuser",]
train <- train[train$USER_ID_hash!="dummyuser",]

ulist$WITHDRAW = 0
ulist[!is.na(ulist$WITHDRAW_DATE),]$WITHDRAW = 1

users <- ulist[,c("USER_ID_hash","SEX_ID","AGE","PREF_NAME","WITHDRAW")]

users<-model.matrix(~ -1 + .,users[,-1],
                    contrasts.arg=lapply(users[,names(which(sapply(users[,-1], is.factor)==TRUE))], contrasts, contrasts=FALSE))

user_with_id <- cbind(ulist$USER_ID_hash,data.frame(users))

write.table(user_with_id,"factor_users.txt",row.names=F,sep="\t")
write.table(train[,-1],"factor_training_coupon.txt",row.names=F,sep="\t")
write.table(test[,-1],"factor_testing_coupon.txt",row.names=F,sep="\t")