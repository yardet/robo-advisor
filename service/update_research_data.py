from impl.user import User
from service.util import data_management, research
from service.config import settings



if __name__ == '__main__':
    # TODO filter with volume
    research.download_data_for_research(settings.NUM_OF_YEARS_HISTORY)
    # research.find_good_stocks()

