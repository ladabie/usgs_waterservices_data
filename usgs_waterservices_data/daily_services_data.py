import requests
import pandas
import re

class WaterStationDailyData():
    """This is a class for Water Station Data from the USGS Water API for daily
    values of data at various water stations across USA
    (https://waterservices.usgs.gov/rest/DV-Service.html).

    Attributes
    ----------
    station_numbers : type
        Description of parameter `station_numbers`.
    geographic_boundary_box : type
        Description of parameter `geographic_boundary_box`.
    date_range : type
        Date range for data to be pulled for. Should be in list format
        with start_date followed by end date. Date format should abide
        by ISO-8601 format (YYYY-MM-DD). Hours. minutes, seconds and
        timezone values are not allowed.
    """

    def __init__(self,date_range,station_numbers=None,geo_boundary_box=None
                 ,us_state=None,us_counties=None):
        """The constructor for WaterStationData

        Parameters
        ----------
        station_numbers : type
            The station number or a list of station numbers to have data
            returned for.
        geo_boundary_box : type
            A list of coordinates to be used to draw an area in which all
            water data should be returned.

        """
        self.station_numbers = station_numbers
        self.geo_boundary_box = geo_boundary_box
        self.us_state = us_state
        self.us_counties = us_counties
        self.date_range = date_range

    def get_data_return_dataframe(self):
        """ A  function to execute building url, fetching data, and
        returns a dataframe with all data.
        """

        self.build_api_url()
        self.fetch_data()
        self.convert_json_to_dataframes()
        return self.water_dataframe

    def build_api_url(self):
        """ A function to build the API url for fetching the USGS water
        station data from the USGS Water Services API for Daily Values.
        """
        base_url = "https://waterservices.usgs.gov/nwis/dv/?format=json&"
        self.__create_major_filter()
        self.__parse_start_end_dates()
        self.complete_url = (base_url
                        + self.major_filter
                        + self.start_date + self.end_date)


    def fetch_data(self):
        """ A function to fetch data using the complete url to return
        json from USGS water services API for daily values.

        """
        print("Fetching Data from USGS Water Services API")
        self.response = requests.get(self.complete_url)
        self.response.raise_for_status()


    def convert_json_to_dataframes(self):
        """ A function to convert json with different datasets
        and combine data into dataframes. Returns a dictionary
        of dataframes.

        """
        print("Converting Data into Dataframe.")
        json_data = self.response.json()
        complete_df = pandas.DataFrame()
        for data in json_data['value']['timeSeries']:
            location = data['sourceInfo']['siteCode'][0]['value']
            metric = data['variable']['variableName'].split(',')[0].lower()
            units= data['variable']['unit']['unitCode'].lower()
            statistic = data['variable']['options']['option'][0]['value'].lower()

            temp_data_load=pandas.DataFrame(data['values'][0]['value'])
            try:
                temp_data_load.drop(columns='qualifiers', inplace=True)
            except:
                pass
            column_name='{stat} {metric} ({units})'.format(stat=statistic
                                                     ,metric=metric
                                                     ,units=units)
            if 'value' not in temp_data_load.columns:
                pass
            else:
                temp_data_load.rename(columns={'dateTime':'date'
                                               ,'value': column_name}
                                      ,inplace=True)
                temp_data_load['date'] = pandas.to_datetime(temp_data_load['date'])
                temp_data_load['location'] = location

                #Check if location already exists in df
                if complete_df.empty:
                    complete_df = temp_data_load
                elif ((complete_df['location'].isin([location]).any()) &
                      (column_name in complete_df.columns)):
                    complete_df.update(temp_data_load)
                elif (complete_df['location'].isin([location]).any()):
                    complete_df=complete_df.merge(temp_data_load, how='outer', on=['location','date'])
                else:
                    complete_df=complete_df.append(temp_data_load,sort=True)

            self.water_dataframe = complete_df



    def __create_major_filter(self):
        """A function to identify which major filter to use for the url
        construction. Only 1 major filter (station numbers, geographic
        boundary, us_state, us_counties) can be used to return station
        data and will be chosen by the previously listed heirarchy if
        multiple are given.
        """
        if self.station_numbers:

            self.major_filter = ("&sites="
                            +self.__converting_list_to_string(self.station_numbers)
                            )
            return
        elif self.geo_boundary_box:
            self.major_filter =("&bBox="
                           +self.__converting_list_to_string(self.geo_boundary_box)
                           )
            return
        elif self.us_state:

            self.major_filter = "&stateCd="+self.us_state
            return
        elif self.us_counties:

            self.major_filter = ("&countyCd="
                            +self.__coverting_list_to_string(self.us_counties)
                            )
            return
        else:
            raise Exception("""No major filter provided.
                            Please update with major filter.""")

    def __converting_list_to_string(self,list_to_convert):
        """A function to convert a list of numbers to a comma separated
        string.

        """
        converted_string=','.join(map(str, list_to_convert))

        return converted_string

    def __parse_start_end_dates(self):
        """ A function to parse the start dates and end dates.
        self.date_range should be in list format [start_date, end_date]
        """
        year_string_format = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')

        self.start_date = "&startDT="+self.date_range[0]
        self.end_date = "&endDT="+self.date_range[-1]
