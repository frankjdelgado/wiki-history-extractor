from db_connector import RevisionDB
import datetime

class QueryHandler(object):
    data={}
    #function which get the quantity of revisions

    #tested
    @classmethod
    def filter_by_user(self,values):
        #values is a list composed by 1 value, the user name to filter by
        data={'user':values[0]}
        return data
    
    @classmethod
    def filter_by_tag(self,values):
        #values is a list composed by 1 value, the tag to filter by
        #NOTE: if necesary, it can be added a functionality to filter by multiple tags with logical OR, AND, XOR, etc.
        data={'tags':values[0]}
        return data

    @classmethod
    def filter_by_size(self,values):
        #values is a list composed by 2 values, the size to filter by, and the order of filtering
        # when the order is greater than 0, it will return the revisions which size are greater than the argument
        # when the order is lesser than 0, it will return the revisions which size are lesser than the argument
        # if the order is 0, it will return the revisions which size are exactly as the argument
        if values[1] > 0:
            data={'size': {'$gt': values[0]} }
        elif values[1] < 0:
            data={'size': {'$lt': values[0]} }
        else:
            data={'size':values[0] }
        return data

    @classmethod
    def filter_by_date(self,values):
        date_format = '%Y-%m-%d'
        #values is a list composed by 1 or 2 values: 
        # date arguments must be in format: YYYY-MM-DD
        # 1 value: one date. It will return the revisions made that date.
        # 2 values: two dates. It will return the revisions made between those dates, inclusive
        # 2 values: one date and one integer. 
        # If the integer is -1: It will return the revisions made from the first revision until the date.
        # If the integer is 1: It will return the revisions made from the date until the last revision.
        # the strptime convert the string arguments into datetime datatype
        if len(values) == 1:
            date_i=datetime.datetime.strptime(values[0],date_format)
            #it is used 2 dates to extract the revision for the whole day, from 0:0 to 23:59
            date_f=date_i.replace(hour=23,minute=59,second=59)
            data={'timestamp': {'$gte':date_i , '$lte':date_f} }
            return data
        elif len(values) == 2:
            #if the second argument is a date:
            if values[1] != 1 and values[1] != -1 :
                date_i=datetime.datetime.strptime(values[0],date_format)
                date_f=datetime.datetime.strptime(values[1],date_format)
                #the date values are adjusted to take into account the day until 23:59
                date_f=date_f.replace(hour=23,minute=59,second=59)
                data={'timestamp': {'$gte':date_i , '$lte':date_f} }
                return data
            else:
                if values[1] == 1:
                    date=datetime.datetime.strptime(values[0],date_format)
                    data={'timestamp': {'$gte':date} }
                    return data
                else:
                    date=datetime.datetime.strptime(values[0],date_format)
                    #the date values are adjusted to take into account the day until 23:59
                    date=date.replace(hour=23,minute=59,second=59)
                    data={'timestamp': {'$lte':date} }
                    return data

    @classmethod
    def filter_by(self,attribute,values):
        if attribute == 1:
            query= self.filter_by_user(values)
        elif attribute == 2:
            query= self.filter_by_tag(values)
        elif attribute == 3:
            query= self.filter_by_size(values)
        elif attribute == 4:
            query= self.filter_by_date(values)
        else:
            print 'Wrong Filter Option'
        return query
        
    @classmethod
    def get_count(self,filter_by_attribute,values):
        data=self.filter_by(filter_by_attribute,values)
        return RevisionDB.count(data)


    @classmethod
    #test method for inserting formatted timestamps
    def insert_dates(self):
        RevisionDB.insert_date()
        

