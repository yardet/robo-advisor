from typing import Callable

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.response import TemplateResponse
from django.test import Client
from django.urls import reverse

from accounts.models import CustomUser, InvestorUser
from core.models import QuestionnaireA, QuestionnaireB
from tests import helper_methods


@pytest.mark.django_db
class TestPreferencesForm:
    # URLS
    url_1: str = 'capital_market_algorithm_preferences_form'
    url_2: str = 'capital_market_investment_preferences_form'
    # TEMPLATES
    template_1: str = 'core/capital_market_algorithm_preferences_form.html'
    template_2: str = 'core/capital_market_investment_preferences_form.html'

    class TestCapitalMarketAlgorithmPreferencesForm:
        def test_successful_get_request_as_logged_user_without_questionnaire_a(self, client: Client,
                                                                               user_factory: Callable):
            response, _ = helper_methods.successful_get_request_as_logged_user(
                client, user_factory, url_name=TestPreferencesForm.url_1, template_src=TestPreferencesForm.template_1
            )
            # Assert attributes
            helper_methods.assert_attributes(response, attributes=[
                'Completing the survey is', 'essential', 'for using our website and AI algorithm', 'Submit',
                'Capital Market Preferences Form - Algorithms',
                'Question #1: Would you like to use machine learning algorithms for stock market investments?',
                'Question #2: Which statistic model would you like to use for stock market investments?',
                'div_id_ml_answer', 'div_id_model_answer',
            ])

        def test_successful_get_request_as_logged_user_with_questionnaire_a(self, client: Client,
                                                                            user_factory: Callable,
                                                                            questionnaire_a_factory: Callable):
            TestPreferencesForm.sign_in(client, user_factory, questionnaire_a_factory)
            response: TemplateResponse = client.get(reverse(TestPreferencesForm.url_1))
            # Assert attributes
            helper_methods.assert_attributes(response, attributes=[
                'Update your capital market algorithm preferences form', 'Update',
                'Capital Market Preferences Form - Algorithms',
                'Question #1: Would you like to use machine learning algorithms for stock market investments?',
                'Question #2: Which statistic model would you like to use for stock market investments?',
                'div_id_ml_answer', 'div_id_model_answer',
            ])

        def test_redirection_get_request_as_guest(self, client):
            helper_methods.redirection_get_request_as_guest(client, url_name=TestPreferencesForm.url_1)

        def test_form_successful_post_request(self, client: Client, user_factory: Callable,
                                              questionnaire_a_factory: Callable):
            user: CustomUser = helper_methods.login_user(client, user_factory)
            # Testing the user form is not within the DB
            with pytest.raises(ObjectDoesNotExist):
                QuestionnaireA.objects.get(user=user)
            data = {
                'ml_answer': '1',
                'model_answer': '1',
            }
            # Testing we are redirected and the new user form is within the DB
            helper_methods.post_request(client, url_name=TestPreferencesForm.url_1, data=data, status_code=200)
            assert QuestionnaireA.objects.get(user=user) is not None
            # GET request to Investment Preferences form
            response: TemplateResponse = helper_methods.successful_get_request_as_guest(
                client, url_name=TestPreferencesForm.url_2, template_src=TestPreferencesForm.template_2
            )
            questionnaire_a: QuestionnaireA = QuestionnaireA.objects.get(user=user)
            ml_answer: int = questionnaire_a.ml_answer
            model_answer: int = questionnaire_a.model_answer
            graph_img_prefix: str = f'/static/img/graphs/1/{ml_answer}{model_answer}'
            helper_methods.assert_attributes(response, attributes=[
                f'{graph_img_prefix}/distribution_graph.png', f'{graph_img_prefix}/three_portfolios.png'
            ])

        def test_form_failure_post_request(self, client: Client, user_factory: Callable,
                                           questionnaire_a_factory: Callable):
            user: CustomUser = helper_methods.login_user(client, user_factory)
            # Testing the user form is not within the DB
            with pytest.raises(ObjectDoesNotExist):
                QuestionnaireA.objects.get(user=user)
            response: TemplateResponse = helper_methods.post_request(
                client, url_name=TestPreferencesForm.url_1, data={}, status_code=200
            )
            # Checking we are in the same template
            template = Template(response.content.decode('utf-8'))
            context = Context(response.context)
            rendered_template = template.render(context)

            # Assert that the template contains the form elements
            for attribute in ['div_id_ml_answer', 'div_id_model_answer']:
                assert attribute in rendered_template

    class TestCapitalMarketInvestmentPreferencesForm:
        def test_successful_get_request_as_logged_user_without_questionnaire_b(self, client: Client,
                                                                               user_factory: Callable,
                                                                               questionnaire_a_factory: Callable):
            _, questionnaire_a = TestPreferencesForm.sign_in(client, user_factory, questionnaire_a_factory)
            ml_answer: int = questionnaire_a.ml_answer
            model_answer: int = questionnaire_a.model_answer
            response: TemplateResponse = client.get(reverse(TestPreferencesForm.url_2))
            helper_methods.assert_successful_status_code_for_get_request(
                response=response, template_src=TestPreferencesForm.template_2
            )
            # Assert attributes
            helper_methods.assert_attributes(response, attributes=[
                'Completing the survey is', 'essential', 'for using our website and AI algorithm', 'Submit'
            ])
            self.assert_attributes(response, graph_img_prefix=f'/static/img/graphs/1/{ml_answer}{model_answer}')

        def test_get_request_as_logged_user_with_questionnaire_b(self, client: Client, user_factory: Callable,
                                                                 questionnaire_a_factory: Callable,
                                                                 questionnaire_b_factory: Callable):
            user, questionnaire_a = TestPreferencesForm.sign_in(client, user_factory, questionnaire_a_factory)
            questionnaire_b_factory(user=user)
            ml_answer: int = questionnaire_a.ml_answer
            model_answer: int = questionnaire_a.model_answer
            response: TemplateResponse = client.get(reverse(TestPreferencesForm.url_2))
            helper_methods.assert_successful_status_code_for_get_request(
                response=response, template_src=TestPreferencesForm.template_2
            )
            # Assert attributes
            helper_methods.assert_attributes(response, attributes=[
                'Update your capital market investment preferences form', 'Update'
            ])
            self.assert_attributes(response, graph_img_prefix=f'/static/img/graphs/1/{ml_answer}{model_answer}')

        @staticmethod
        def assert_attributes(response: TemplateResponse, graph_img_prefix: str) -> None:
            helper_methods.assert_attributes(response, attributes=[
                'Capital Market Preferences Form - Investments',  # Attribute
                'Question #1: For how many years do you want to invest?',  # Attribute
                'Question #2: Which distribution do you prefer?',  # Attribute
                'Question #3: What is your preferable graph?',  # Attribute
                'div_id_answer_1', 'div_id_answer_2', 'div_id_answer_3',  # Attributes
                f'{graph_img_prefix}/distribution_graph.png',  # Image
                f'{graph_img_prefix}/three_portfolios.png',  # Image
            ])

        def test_redirection_get_request_as_guest(self, client):
            helper_methods.redirection_get_request_as_guest(client, url_name=TestPreferencesForm.url_2)

        def test_page_not_found_get_request_as_logged_user(self, client: Client, user_factory: Callable):
            """
            We expect to get 4xx response code, because there is no instance of `QuestionnaireA`
            """
            helper_methods.page_not_found_get_request_as_logged_user(
                client, user_factory, url_name=TestPreferencesForm.url_2
            )

        def test_form_successful_post_request(self, client: Client, user_factory: Callable,
                                              questionnaire_a_factory: Callable):
            user, _ = TestPreferencesForm.sign_in(client, user_factory, questionnaire_a_factory)
            with pytest.raises(ObjectDoesNotExist):
                QuestionnaireB.objects.get(user=user)
            data = {f'answer_{i}': '3' for i in range(1, 4)}
            # Testing we are redirected
            helper_methods.post_request(client, url_name=TestPreferencesForm.url_2, data=data, status_code=200)
            # Testing the new user form is within the DB
            assert QuestionnaireB.objects.get(user=user) is not None

        def test_form_failure_post_request(self, client: Client, user_factory: Callable,
                                           questionnaire_a_factory: Callable):
            user, _ = TestPreferencesForm.sign_in(client, user_factory, questionnaire_a_factory)
            with pytest.raises(ObjectDoesNotExist):
                QuestionnaireB.objects.get(user=user)
            response: TemplateResponse = helper_methods.post_request(
                client, url_name=TestPreferencesForm.url_2, data={}, status_code=200
            )
            # Checking we are in the same template
            template = Template(response.content.decode('utf-8'))
            context = Context(response.context)
            rendered_template = template.render(context)

            # Assert that the template contains the form elements
            for i in range(1, 4):
                assert f'div_id_answer_{i}' in rendered_template

    class TestBothForms:
        def test_forms_successful_post_requests(self, client: Client, user_factory: Callable,
                                                questionnaire_a_factory: Callable):
            user: CustomUser = helper_methods.login_user(client, user_factory)
            # Testing the user form is not within the DB
            with pytest.raises(ObjectDoesNotExist):
                QuestionnaireA.objects.get(user=user)
            self.send_both_questionnaires(client, user)

        def test_forms_successful_post_requests_with_different_stocks_collection_number(
                self, client: Client, user_factory: Callable, investor_user_factory: Callable,
                questionnaire_a_factory: Callable
        ):
            user: CustomUser = helper_methods.login_user(client, user_factory)
            # CREATE - Questionnaire A, then Questionnaire B (which automatically CREATES InvestorUser)
            # Testing the user form is not within the DB
            with pytest.raises(ObjectDoesNotExist):
                QuestionnaireA.objects.get(user=user)
            self.send_both_questionnaires(client, user)
            # Testing investor user data
            investor_user: InvestorUser = InvestorUser.objects.get(user=user)
            assert investor_user.stocks_collection_number == '1'
            data: dict[str, InvestorUser, InvestorUser] = {
                'stocks_collection_number': '2',
                'investor_user_instance': investor_user,
                'instance': investor_user,
            }
            # UPDATE InvestorUser, using Profile Investor Form
            helper_methods.post_request(client, 'profile_investor', data=data, status_code=302)
            # POST
            # Update Preferences Form Again
            self.send_both_questionnaires(client, user, create=False)

        @staticmethod
        def send_both_questionnaires(client, user, create: bool = True):
            data1: dict[str, str] = {
                'ml_answer': '1',
                'model_answer': '1',
            }
            # Testing we are redirected and the new user form is within the DB
            helper_methods.post_request(client, url_name=TestPreferencesForm.url_1, data=data1, status_code=200)
            assert QuestionnaireA.objects.get(user=user) is not None
            # GET request to Investment Preferences form
            helper_methods.successful_get_request_as_guest(
                client, url_name=TestPreferencesForm.url_2, template_src=TestPreferencesForm.template_2
            )
            if create:
                with pytest.raises(ObjectDoesNotExist):
                    QuestionnaireB.objects.get(user=user)
            data2: dict[str, str, str] = {f'answer_{i}': '3' for i in range(1, 4)}
            # Testing we are redirected
            helper_methods.post_request(
                client, url_name=TestPreferencesForm.url_2, data=data2, status_code=200
            )
            # Testing the new user form is within the DB
            assert QuestionnaireB.objects.get(user=user) is not None

    @staticmethod
    def sign_in(client: Client, user_factory: Callable,
                questionnaire_a_factory: Callable) -> tuple[CustomUser, QuestionnaireA]:
        user: CustomUser = helper_methods.login_user(client, user_factory)
        questionnaire_a: QuestionnaireA = questionnaire_a_factory(user=user)
        return user, questionnaire_a
