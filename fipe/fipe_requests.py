
import requests as req

base_url = "https://veiculos.fipe.org.br/api/veiculos"

default_params = {
    'codigoTipoVeiculo': 1,
    'codigoTipoCombustivel': 1,
    'tipoVeiculo': 'carro',
    'tipoConsulta': 'tradicional'
}

def list_brands():
    request_params = default_params.copy()
    request_params['codigoTabelaReferencia'] = last_six_semesters_ids()[0]
    response = req.post(f'{base_url}/ConsultarMarcas', request_params)
    return response.json()


def list_models(brand_id):
    request_params = default_params.copy()
    request_params['codigoMarca'] = brand_id
    request_params['codigoTabelaReferencia'] = last_six_semesters_ids()[0]
    response = req.post(f'{base_url}/ConsultarModelos', request_params)
    return response.json()

def get_years_by_model(brand_id, model_id):
    request_params = default_params.copy()
    request_params['codigoMarca'] = brand_id
    request_params['codigoModelo'] = model_id
    request_params['codigoTabelaReferencia'] = last_six_semesters_ids()[0]
    response = req.post(f'{base_url}/ConsultarAnoModelo', request_params)
    return response.json()


def get_car_info(brand_id, model_id, year):
    car_price_list = []

    for year_reference in last_six_semesters_ids():
        year_info_list = year.split('-')
        request_params = default_params.copy()
        request_params['codigoTabelaReferencia'] = year_reference
        request_params['codigoMarca'] = brand_id
        request_params['codigoModelo'] = model_id
        request_params['anoModelo'] = year_info_list[0]
        request_params['codigoTipoCombustivel'] = year_info_list[1]
        response = req.post(f'{base_url}/ConsultarValorComTodosParametros', request_params)
        json_response = response.json()
        json_car = {
            'price': json_response.get('Valor'),
            'month': json_response.get('MesReferencia'),
            'year_code': year_reference,
            'car_year': json_response.get('AnoModelo'),
            'car_id': model_id
        }
        car_price_list.append(json_car)

    return car_price_list

def last_six_semesters_ids():
    list_ids = []
    response = req.post(f'{base_url}/ConsultarTabelaDeReferencia')
    response_json = response.json()
    for arr_index in range(0, 15):
        month_id = arr_index * 12
        list_ids.append(response_json[month_id]['Codigo'])

    return list_ids
