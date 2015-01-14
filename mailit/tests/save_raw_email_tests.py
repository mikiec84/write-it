# coding=utf8
from global_test_case import GlobalTestCase as TestCase
from global_test_case import ResourceGlobalTestCase as ResourceTestCase
import os
import logging
from mailit.models import RawIncomingEmail
from ..bin.handleemail import EmailHandler
from nuntium.models import WriteItInstance, Answer

class IncomingRawEmailTestCase(TestCase):
    def setUp(self):
        super(IncomingRawEmailTestCase, self).setUp()
        f = open('mailit/tests/fixture/mail.txt')
        self.email_content = f.readlines()
        f.close()

    def test_create_one(self):
        '''Instanciate an incoming raw email'''
        raw_email = RawIncomingEmail(content=self.email_content)
        self.assertTrue(raw_email)
        self.assertEquals(raw_email.content, self.email_content)
        
    def test_it_automatically_saves(self):
        '''It automatically saves the answer when an incoming email arrives'''
        handler = EmailHandler()
        answer = handler.handle(self.email_content)
        raw_emails = RawIncomingEmail.objects.all()
        self.assertTrue(raw_emails)
        self.assertTrue(raw_emails.filter(content=self.email_content))

    def test_it_relates_the_raw_mail_to_an_instance(self):
        '''The raw message can be related to an instance'''
        instance = WriteItInstance.objects.all()[0]
        raw_email = RawIncomingEmail(content=self.email_content)
        raw_email.writeitinstance = instance
        raw_email.save()

        instance = WriteItInstance.objects.get(id=instance.id)
        raw_emails = instance.raw_emails.all()

        self.assertTrue(raw_emails)
        self.assertIn(raw_email, raw_emails)

    def test_can_be_related_to_an_answe(self):
        '''A raw mail can be related to an answer'''
        answer = Answer.objects.all()[0]
        with self.assertRaises(RawIncomingEmail.DoesNotExist) as error:
            answer.raw_email
        raw_email = RawIncomingEmail(content=self.email_content)
        raw_email.answer = answer
        raw_email.save()

        answer = Answer.objects.get(id=answer.id)
        self.assertTrue(answer.raw_email)
        self.assertEquals(answer.raw_email, raw_email)
