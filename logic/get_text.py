# coding=utf-8
import re

import numpy as np
import pandas as pd
from transliterate import translit

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 12000)
pd.set_option('display.width', 1000)


def get_text_from_db():
    return '0'


def get_texts(map_path ,save_path , month):
    fish = pd.read_csv(map_path['db1'] + '/ref/fish.csv', sep=';')
    prod_designate = pd.read_csv(
        map_path['db1'] + '/ref/prod_designate.csv', sep=';')
    prod_type = pd.read_csv(map_path['db1'] + '/ref/prod_type.csv',
                            sep=';')
    regime = pd.read_csv(map_path['db1'] + '/ref/regime.csv',
                         sep=';')
    region = pd.read_csv(map_path['db1'] + '/ref/region.csv',
                         sep=';')
    product = pd.read_csv(map_path["product.csv"], sep=',')
    catch = pd.read_csv(map_path["catch.csv"], sep=',')
    ext = pd.read_csv(map_path['Ext.csv'], sep=',')
    ext2 = pd.read_csv(map_path['Ext2.csv'], sep=',')

    ext2['date_vsd'] = pd.to_datetime(ext2['date_vsd'])
    product['date'] = pd.to_datetime(product['date'])
    catch['date'] = pd.to_datetime(catch['date'])

    def date_filter(month):
        month1 = month + 1
        date = f'2022-0{month}-01'
        date2 = f'2022-0{month1}-01'
        ext1 = ext2.loc[(ext2['date_vsd'] > date) & (ext2['date_vsd'] < date2)]
        product1 = product.loc[(product['date'] > date) & (product['date'] < date2)]
        catch1 = catch.loc[(catch['date'] > date) & (catch['date'] < date2)]
        return ext1, product1, catch1

    ext2, product, catch = date_filter(2)
    fish['id_fish'] = fish['id_fish'] * -1

    name_id = fish[['id_fish', 'fish']]
    df_time = prod_type[['id_prod_type', 'prod_type']].rename(columns={
        'id_prod_type': 'id_fish',
        'prod_type': 'fish'
    })
    name_id = pd.concat([name_id, df_time], ignore_index=True)
    df_time = prod_type[['id_prod_type',
                         'prod_type_full']].rename(columns={
        'id_prod_type': 'id_fish',
        'prod_type_full': 'fish'
    })
    name_id = pd.concat([name_id, df_time], ignore_index=True).dropna()
    df_time = None

    def norm_string(x):
        str_ = re.sub(r'[^а-яА-Я ]', '',
                      translit(x.replace('-', ' ').lower(),
                               'ru')).replace('  ', ' ').replace('  ', ' ')
        return str_

    name_id['fish'] = name_id['fish'].apply(lambda x: norm_string(x))
    ext2['new_name'] = ext2['fish'].apply(lambda x: norm_string(x))
    # делаю чтобы у одинаковых названий был один и тот же id
    name_id_uni = name_id.drop_duplicates(subset=['fish']).rename(
        columns={'id_fish': 'id_fish_uni'})
    name_id = name_id.merge(name_id_uni, on='fish', how='left')
    name_id_uni = None

    soed = product.merge(prod_designate, on='id_prod_designate', how='left')
    soed = soed.merge(prod_type, on='id_prod_type', how='left')
    del soed['prod_board_volume']
    soed['prod_volume'] = soed['prod_volume'] * 1000
    soed['prod_volume'] = soed['prod_volume'].fillna(0).astype(np.int64,
                                                               errors='ignore')
    id_prod_designate = soed.groupby(
        ['id_ves', 'id_prod_type', 'id_fish', 'id_prod_designate'],
        as_index=False)['prod_volume'].sum()

    # Каждой рыбы поймано всего корблём
    soed = catch.merge(fish, on='id_fish', how='left')
    # soed = soed.merge(prod_designate, on='id_prod_designate' , how = 'left')
    # soed = soed.merge(prod_type, on='id_prod_type' , how = 'left')
    soed = soed.merge(regime, on='id_regime', how='left')
    soed = soed[['id_ves', 'id_fish', 'catch_volume']]
    catch_by_id_ves = soed.groupby(['id_ves', 'id_fish'],
                                   as_index=False)['catch_volume'].sum()
    catch_by_id_ves['catch_volume'] = catch_by_id_ves['catch_volume'] * 1000
    catch_by_id_ves['catch_volume'] = catch_by_id_ves['catch_volume'].fillna(
        0).astype(np.int64, errors='ignore')
    # Получем сводную таблицу по рыбам продуктам и массам

    def svodnaya(row):
        list_ = []
        table_of_results = id_prod_designate.loc[
            (id_prod_designate['id_ves'] == row['id_ves'])
            & (id_prod_designate['id_fish'] == row['id_fish'])]
        list0 = table_of_results['id_prod_type'].tolist() + [(row['id_fish'] * -1)]
        list_.append(list0)
        list_.append(table_of_results['prod_volume'].tolist())
        list_of_uni_id = []
        for id_ in list_[0]:
            uni = name_id.loc[(name_id['id_fish'] == id_)]['id_fish_uni'].iloc[0]
            list_of_uni_id.append(uni)
        list_.append(list_of_uni_id)
        if list_ != [[], [], []]:
            return list_
        else:
            return np.nan

    catch_by_id_ves['prod_and_vol'] = catch_by_id_ves.apply(
        lambda row: svodnaya(row), axis=1)
    catch_by_id_ves['products'] = catch_by_id_ves['prod_and_vol'].apply(
        lambda x: x[0] if type(x) == list else np.nan)
    catch_by_id_ves['volumns'] = catch_by_id_ves['prod_and_vol'].apply(
        lambda x: x[1] if type(x) == list else np.nan)
    catch_by_id_ves['id_fish_uni'] = catch_by_id_ves['prod_and_vol'].apply(
        lambda x: x[2] if type(x) == list else np.nan)
    del catch_by_id_ves['prod_and_vol']

    def fish_lasts(row):
        if type(row['volumns']) == list:
            sum_of = int(sum(row['volumns']))
            usl_ost = int(row['catch_volume']) - sum_of
            list_ = row['volumns']
            list_.append(usl_ost)
            return list_
        else:
            return np.nan

    catch_by_id_ves['volumns'] = catch_by_id_ves.apply(lambda row: fish_lasts(row),
                                                       axis=1)

    def new_volumn(row):
        dict_ = {}
        if type(row['id_fish_uni']) == list:
            for index_ in range(len(row['id_fish_uni'])):
                id_fish = row['id_fish_uni'][index_]
                if id_fish not in dict_.keys():
                    dict_[id_fish] = row['volumns'][index_]
                else:
                    dict_[id_fish] = dict_[id_fish] + row['volumns'][index_]
            list_ = [list(dict_.keys()), list(dict_.values())]
            return list_
        else:
            return np.nan

    catch_by_id_ves['new_prod_and_vol'] = catch_by_id_ves.apply(
        lambda row: new_volumn(row), axis=1)

    def new_volumn(row):
        dict_ = {}
        if type(row['id_fish_uni']) == list:
            for index_ in range(len(row['id_fish_uni'])):
                id_fish = row['id_fish_uni'][index_]
                if id_fish not in dict_.keys():
                    dict_[id_fish] = row['volumns'][index_]
                else:
                    dict_[id_fish] = dict_[id_fish] + row['volumns'][index_]
            list_ = []
            for k, v in dict_.items():
                s = [k, v]
                list_.append(s)
            return list_
        else:
            return np.nan

    catch_by_id_ves['for_expl'] = catch_by_id_ves.apply(
        lambda row: new_volumn(row), axis=1)

    catch_by_id_ves['products_uni'] = catch_by_id_ves['new_prod_and_vol'].apply(
        lambda x: x[0] if type(x) == list else np.nan)
    catch_by_id_ves['volumns_uni'] = catch_by_id_ves['new_prod_and_vol'].apply(
        lambda x: x[1] if type(x) == list else np.nan)
    # %%
    catch_exp = catch_by_id_ves[['id_ves', 'id_fish', 'catch_volume', 'for_expl']]
    catch_exp = catch_exp.explode('for_expl')
    catch_exp['product_uni'] = catch_exp['for_expl'].apply(
        lambda x: x[0] if type(x) == list else np.nan)
    catch_exp['volumn_uni'] = catch_exp['for_expl'].apply(
        lambda x: x[1] if type(x) == list else np.nan)
    del catch_exp['for_expl']
    catch_exp = catch_exp.drop_duplicates()

    ext1 = ext[['id_ves', 'id_own', 'id_vsd', 'id_Plat']]
    ext3 = ext2.merge(ext1, left_on='id_vsd', right_on='id_vsd', how='left')
    ext3 = ext3.merge(name_id, left_on='new_name', right_on='fish', how='left')
    ext3 = ext3[['id_ves', 'id_vsd', 'num_vsd', 'volume', 'new_name', 'id_fish_uni']]
    gr_ext = ext3.groupby(by=['id_ves', 'id_fish_uni', 'new_name'],
                          as_index=False)['volume'].sum()
    gr_ext = gr_ext.drop_duplicates()
    gr_ext['id_fish_uni'] = gr_ext['id_fish_uni'].astype(np.int64, errors='ignore')
    final_volumns = catch_exp.merge(gr_ext, left_on=['id_ves', 'product_uni'], right_on=['id_ves', 'id_fish_uni'],
                                    how='outer')
    no_exp = final_volumns[final_volumns['volume'].isna()]
    no_id_fish = final_volumns[final_volumns['id_fish'].isna()]
    len_no_exp = len(no_exp)
    len_no_id_fish = len(no_id_fish)
    final_volumns = catch_exp.merge(gr_ext, left_on=['id_ves', 'product_uni'], right_on=['id_ves', 'id_fish_uni'],
                                    how='inner')
    different = final_volumns.loc[(final_volumns['id_fish'] != -final_volumns['id_fish_uni'])]

    len_different = len(different)
    different = different[['id_ves', 'id_fish', 'id_fish_uni', 'new_name']]
    different['id_fish'] = -different['id_fish']
    different = different.merge(name_id, left_on='id_fish', right_on='id_fish', how='left')

    different = different[['id_ves',
                           'new_name', 'fish', 'id_fish', 'id_fish_uni_x']].rename(columns={
        'id_ves': 'Номер судна',
        'new_name': 'Поступило в продажу', 'fish': 'Было выловлено', 'id_fish': 'ID выловлено',
        'id_fish_uni_x': 'ID поступило в продажу',
    })
    final_volumns = final_volumns.merge(name_id, on='id_fish_uni', how='left')
    final_volumns['id_fish_y'] = abs(final_volumns['id_fish_y'])
    final_volumns['id_fish_y'] = abs(final_volumns['id_fish_uni'])
    different = final_volumns.loc[(final_volumns['id_fish_x'] != final_volumns['id_fish_uni'])].dropna()
    ################# RESULT
    final_text = f'Результаты: за данный период в данных отсутсвуют продажи по следующим выловленным сырьём {len_no_exp}. Подробнее в файле "Нет продаж". Отсутсвуют данные о вылове для {len_no_id_fish}, хотя были продажи.Подробнее в файле "Нет вылова" Таже следует обратить внимание на {len_different} судов, у которых проданные продукты не соотвествовали тосу сырью которе выловили.Подробнее в файле "Несоответсвие".'
    different.to_csv(f"{save_path}/Несоответсвие.csv", index=False, encoding='utf-8', sep=';')
    no_exp.to_csv(f"{save_path}/Нет_продаж.csv", index=False, encoding='utf-8')
    no_id_fish.to_csv(f"{save_path}/Нет_вылова.csv", index=False, encoding='utf-8')

    return  final_text
