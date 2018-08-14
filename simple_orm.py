import sqlite3


class MyDataBase():

    def __init__(self, db):
        self.database = db
        self.connect = sqlite3.connect(self.database)
        self.dbcursor = self.connect.cursor()


    def get_where_parameters(datatoupdate):
        whereparamiters = datatoupdate.pop('where')
        return whereparamiters


    def write_columns_to_select(columns):
        strcolumns = ','.join(columns)
        return strcolumns


    def write_paramiters_to_insert(paramiterstoinsert):
        parameters = []
        for key in paramiterstoinsert.keys():
            parameters.append(str(key))
        strinofparamiters = ', '.join(parameters)
        return '(' + strinofparamiters + ')'


    def get_values(alldataparamiters):
        return [alldataparamiters[key] for key in alldataparamiters]


    def union_values_for_cimmit(dataforupdate, dataforsearchinbase):
        return [dataforupdate[key] for key in dataforupdate] + [dataforsearchinbase[key] for key in dataforsearchinbase]


    def write_string_paramiters(searchparamiters):
        parameters = ''
        for key in searchparamiters.keys():
            parameters = parameters + str(key) + ' =?,'
        return parameters[:-1]


    def create_table(self, tablename, *columns):
        self.dbcursor.execute('CREATE TABLE %(table)s %(columns)s' % {'table': tablename, 'columns': columns})
        self.connect.commit()


    def drop_table(self, tablename):
        self.dbcursor.execute('drop table if exists %(table)s' % {'table': tablename})
        self.connect.commit()


    def insert(self, tablename, **datatoinsert):
        columns = MyDataBase.write_paramiters_to_insert(datatoinsert)
        values = MyDataBase.get_values(datatoinsert)
        queryparamiters = ('?,' * len(datatoinsert))[:-1]
        querystring = 'INSERT INTO %(table)s %(columns)s VALUES(\
        ' % {'table': tablename, 'columns': columns} + queryparamiters + ')'
        self.dbcursor.execute(querystring, values)
        self.connect.commit()


    def update(self, tablename, **updatedata):
        dictwhereparamiters = MyDataBase.get_where_parameters(updatedata)
        paramtosearch = MyDataBase.write_string_paramiters(dictwhereparamiters)
        columnnames = MyDataBase.write_string_paramiters(updatedata)
        valuestochange = MyDataBase.union_values_for_cimmit(updatedata, dictwhereparamiters)
        querystrig = ('UPDATE %(nametable)s SET %(columns)s WHERE %(where)s' % {'nametable': tablename, 'columns': columnnames, 'where': paramtosearch}
        )
        self.dbcursor.execute(querystrig, valuestochange)
        self.connect.commit()


    def select(self, tablename, *columns):
        strcolumns = MyDataBase.write_columns_to_select(columns)
        self.dbcursor.execute('SELECT %(columns)s FROM %(table)s' \
        % {'table': tablename, 'columns': strcolumns})
        return self.dbcursor.fetchall()


    def select_all(self, tablename):
        self.dbcursor.execute('SELECT * FROM %(table)s' % {'table': tablename})
        return self.dbcursor.fetchall()



if __name__ == '__main__':

    mybase = MyDataBase('database.db')
    mybase.create_table('table1', 'col1', 'col2')
    mybase.insert('table1', col1='foo', col2='bar')
    mybase.update('table1', col1='bar', col2='foo', where={'col1':'foo'})
    print(mybase.select_all('table1'))
    print(mybase.select('table1', 'col1'))
    mybase.drop_table('table1')
