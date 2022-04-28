import json


with open('city_list.json', 'r') as f_json:
    data = f_json.read()

reg_list = []
end_json = []
obj = json.loads(data)
pk_reg = 0
pk_city = 0
pk_reg_city = 0

for reg_city in obj:

    reg = reg_city['region']
    if reg not in reg_list:
        pk_reg += 1
        reg_list.append(reg)
        end_json.append({
            'model': 'location.region',
            'pk': pk_reg,
            'fields':
                {'region': reg}
        })
    city = reg_city['city']
    pk_city += 1
    pk_reg_city += 1
    end_json.append({
        'model': 'location.city',
        'pk': pk_city,
        'fields':
            {'city': city}
    })

    end_json.append(
        {
            'model': 'location.regioncity',
            'pk': pk_reg_city,
            'fields':
                {'region': pk_reg,
                 'city': pk_city}
        }
    )

with open('fixture.json', 'w', encoding='utf-8') as new_f_json:
    json.dump(end_json,new_f_json,ensure_ascii=False,indent=4)

print('done')
