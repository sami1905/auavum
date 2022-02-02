import dash_html_components as html
import base64
import io
import sys
import pandas as pd

def getFilename(img, name):
    if img[0] is None:
        children=[]
        for i in name:
            children.append(html.Li(i, className='card-text3', style={'padding':'0', 'margin':'0'}))
        return html.Ul(children) 
    else:
        children=[]
        for i in name:
            item={'label': i, 'value': name.index(i)}
            children.append(item)
        return children

# return uploaded content as dataframe
def content2df(contents, filename, date):
    content_type, content_string = contents.split(',')
    file_size= ((sys.getsizeof(contents)/1024)/1024)
    #print(filename + ': ' + str(file_size) + ' MB')
    decoded = base64.b64decode(content_string)

    try:
        if '.csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('latin1')), sep=';', low_memory=False)
            list = [df, filename]
            file_size= ((sys.getsizeof(df)/1024)/1024)
            #print('DataFrame: ' + str(file_size) + ' MB')
            return list
        elif '.xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            file_size= ((sys.getsizeof(df)/1024)/1024)
            #print('DataFrame: ' + str(file_size) + ' MB')
            list = [df, filename]
            return list
        elif '.xls' not in filename and '.csv' not in filename:
            return filename
    except Exception as e:
        print(e)
        return filename