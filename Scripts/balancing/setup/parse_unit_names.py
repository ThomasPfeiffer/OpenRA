from balancing.utility.yaml_util import parse_yaml_file

def main():
    filenames = ['aircraft.yaml', 'infantry.yaml', 'ships.yaml' , 'structures.yaml']
    for filename in filenames:
        yaml = parse_yaml_file(filename)
        print(yaml)
        with open('all_'+filename, 'w') as f:
            for k,v in yaml.iteritems():
                if not 'Tooltip' in v:
                    abc = v['DisguiseToolTip']['Name']['self']
                else :
                    abc = v['Tooltip']['Name']['self']
                s = k + '\t' + abc + '\n'
                f.write(s)
                print(s)
    print("finished")

if __name__ == "__main__":
    main()