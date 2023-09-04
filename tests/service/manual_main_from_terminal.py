import pytest

from service.config import settings
from service.impl.user import User
from service.util import data_management, research


@pytest.mark.django_db
class TestManualMainFromTerminal:
    user_id: int = -1
    user_name: str = 'test'  # data_management.get_name()
    data_changed = False
    is_machine_learning: int = 1
    model_option: int = 1  # gini
    stocks_collection_number: str = "1"  # 1 default
    stock_name: str = 'AAPL'
    num_of_years_history: int = 10
    show_result: bool = False

    def test_creates_new_user(self):

        stocks_symbols = data_management.get_stocks_symbols_from_collection(self.stocks_collection_number)
        # sub_folder = f'{self.stocks_collection_number}/{self.is_machine_learning}{self.model_option}/'
        # Extended data from datasets (CSV Tables)
        tables = data_management.get_extended_data_from_db(
            stocks_symbols, self.is_machine_learning, self.model_option, self.stocks_collection_number,
        )
        sectors_data, sectors, closing_prices_table, three_best_portfolios, three_best_sectors_weights, \
            pct_change_table, yield_list = tables
        first_question_score = 2  # medium risk
        second_question_score = 2  # medium risk
        third_question_score = 2  # medium risk
        sum_of_score = first_question_score + second_question_score + third_question_score
        level_of_risk = data_management.get_level_of_risk_by_score(sum_of_score)

        # creates new user with portfolio details
        portfolio = data_management.create_new_user_portfolio(
            stocks_symbols=stocks_symbols,
            investment_amount=0,
            is_machine_learning=self.is_machine_learning,
            stat_model_name=settings.MODEL_NAME[self.model_option],
            risk_level=level_of_risk,
            extended_data_from_db=tables,
        )

        user: User = User(
            _id=self.user_id, _name=self.user_name, _portfolio=portfolio,
            _stocks_collection_number=self.stocks_collection_number
        )
        try:
            investments_list = data_management.get_user_investments_from_json_file(self.user_name)
            data_management.changing_portfolio_investments_treatment_console(user.portfolio, investments_list)
        except Exception as e:
            print(e)
        # add user to datasets (json file)
        user.update_json_file(settings.USERS_JSON_NAME)
        data_management.save_user_portfolio(user)

    def test_add_investment(self):
        investment_amount: int = 500
        if investment_amount is not None:
            __, investments_list = data_management.add_new_investment(self.user_name, investment_amount)

        if self.show_result:
            data_management.plot_investments_history(self.user_id, investments_list)

    def test_plot_user_portfolio_graphs(self):
        # TODO: this test fails
        # json_data = data_management.get_json_data(settings.USERS_JSON_NAME)
        # collection_number = json_data['usersList'][self.user_name][0]['stocksCollectionNumber']
        user_instance = data_management.get_user_from_db(self.user_id, self.user_name)
        data_management.save_user_portfolio(user_instance)

        if self.show_result:
            data_management.plot_image(f'{settings.USER_IMAGES}{self.user_id}/sectors_weights_graph.png')
            data_management.plot_image(f'{settings.USER_IMAGES}{self.user_id}/stocks_weights_graph.png')
            data_management.plot_image(f'{settings.USER_IMAGES}{self.user_id}/estimated_yield_graph.png')

    def test_forecast_specific_stock(self):
        models_data: dict = data_management.get_models_data_from_collections_file()
        for i in range(len(settings.MACHINE_LEARNING_MODEL)):

            plt_instance = research.forecast_specific_stock(str(self.stock_name), settings.MACHINE_LEARNING_MODEL[i],
                                                            models_data, self.num_of_years_history)
            operation = '_forecast'
            research.save_user_specific_stock(self.stock_name, operation, plt_instance)

            if self.show_result:
                data_management.plot_image(
                    settings.RESEARCH_IMAGES + self.stock_name + operation + '.png'
                )

    def test_bb_strategy(self):

        staring_date, today_date = data_management.get_from_and_to_date(self.num_of_years_history)
        plt_instance = research.plot_bb_strategy_stock(str(self.stock_name), staring_date, today_date)
        operation = '_bb_strategy'
        research.save_user_specific_stock(self.stock_name, operation, plt_instance)

        if self.show_result:
            data_management.plot_image(
                settings.RESEARCH_IMAGES + self.stock_name + operation + '.png')

    def test_top_stock_sector(self):
        filters = [0, 1000000000000, 4, 30, 0.5, 1500]
        sector_name = "US stocks"
        data_tuple = research.find_good_stocks(sector_name)
        sorted_data_tuple, intersection = research.sort_good_stocks(data_tuple, filters)
        data_management.plot_research_graphs(sorted_data_tuple, intersection, sector_name)
        prefix_str = 'top_stocks_'

        if self.show_result:
            data_management.plot_image(f'{settings.RESEARCH_IMAGES}{prefix_str}{sector_name}.png')

    def test_stat_model_scatter_graph(self):
        sub_folder = f'{str(self.stocks_collection_number)}/{str(self.is_machine_learning)}{str(self.model_option)}/'
        stocks_symbols = data_management.get_stocks_symbols_from_collection(self.stocks_collection_number)
        closing_prices_table_path = f'{settings.BASIC_STOCK_COLLECTION_REPOSITORY_DIR}{self.stocks_collection_number}/'
        data_management.plot_stat_model_graph(
            stocks_symbols=stocks_symbols, is_machine_learning=self.is_machine_learning,
            model_name=settings.MODEL_NAME[self.model_option], num_of_years_history=self.num_of_years_history,
            closing_prices_table_path=closing_prices_table_path, sub_folder=sub_folder)

        if self.show_result:
            model_name: str = settings.MODEL_NAME[self.model_option]
            data_management.plot_image(f'{settings.GRAPH_IMAGES}{sub_folder}{model_name}_all_options.png')