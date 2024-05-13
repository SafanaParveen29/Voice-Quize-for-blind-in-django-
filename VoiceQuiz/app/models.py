from django.db import models

class UserDetail(models.Model):
	name = models.CharField('Name', max_length=255)
	email_id = models.EmailField('Email Id', max_length=255)
	phone_number = models.CharField('Mobile Number', max_length=50,null=True,blank=True)
	address = models.TextField('Address',null=True,blank=True)
	country = models.CharField('Country', max_length=100,default='India')
	state = models.CharField('State', max_length=100,default='Tamil Nadu')
	city = models.CharField('City', max_length=100,null=True,blank=True)
	quiz_id = models.CharField('Username', max_length=100, unique=True,null=True)
	def __str__(self):
		return self.name
class Quiz_Question(models.Model):
	question = models.CharField('Question', max_length=255)
	option1 = models.CharField('Option1', max_length=255)
	option2 = models.CharField('Option2', max_length=255)
	option3 = models.CharField('Option3', max_length=255)
	option4 = models.CharField('Option4', max_length=255)
	answer = models.CharField('Answer', max_length=255)
	def __str__(self):
		return self.question
class Answer_Detail(models.Model):
	question = models.IntegerField(null=True)
	rand_num = models.CharField(max_length=255)
	ans = models.CharField('Answer', max_length=255)
	user_id = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.user_id)+" - "+ "Question Number : " + str(self.question)+" - "+ " Answer : " +str(self.ans)+ " - "+ " Quiz Id: "+str(self.rand_num)
		

