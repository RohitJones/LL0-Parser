# Limitations: Ignores epsilon in first and therefore follow is useless. Did not add $ to terminals

from collections import OrderedDict
import copy

first_dict = OrderedDict()
follow_dict = OrderedDict()
grammar = []                                                # store the various rules of the grammar
Parsing_Grammar = []
Non_Terminals = []                                          # store the non terminals of the grammar
Terminals = []

non_terminal_dict = OrderedDict()
terminal_dict = OrderedDict()


def create_both_dicts():
    i = 0
    for each in Non_Terminals:
        non_terminal_dict[each] = i
        i += 1

    i = 0
    for each in Terminals:
        terminal_dict[each] = i
        i += 1


def write_dictionary(passed_dictionary, string_to_print, output_file_name):
    with open(output_file_name, "a") as file_ptr:
        file_ptr.write("\n")

        for each in passed_dictionary:                              # write the dictionary
            temp = string_to_print + "(" + each + ") = {"           # to an output file
                                                                    # according to the
            for item in passed_dictionary[each]:                          # format
                temp = temp + item[0] + ", "  # follow(Non-Terminal) = { Terminals }
            temp = temp.rstrip(', ')                                #
            temp += "}\n"                                           #
            file_ptr.write(temp)                                    #


def get_grammar(input_file_name,output_file_name):
    inputfile = open(input_file_name, 'r')
    outputfile = open(output_file_name, 'w')

    Line_counter = 0
    for line in inputfile:                                      # read the input file containing the grammar
        for each in line:
            if each.islower():
                Terminals.append(each)

        outputfile.write(line)                                  # write the grammer rules to the output file
        grammar.append(("%d " +line.strip().split("\n")[0]) % Line_counter)                # store each line of input into grammar
        Line_counter += 1
    # print(grammar)
    inputfile.close()
    outputfile.close()


def create_table():
    create_both_dicts()

    Parsing_table = [[0 for x in range(len(Terminals))] for x in range(len(Non_Terminals))]
    for x in range(len(Non_Terminals)):
        for y in range(len(Terminals)):
            Parsing_table[x][y] = -1

    for each_nonterminal in Non_Terminals:
        temp = first_dict[each_nonterminal]
        for each in temp:
            Parsing_table[non_terminal_dict[each_nonterminal]][terminal_dict[each[0]]] = int(each[1])

    for each in grammar:
        Parsing_Grammar.append(each[5:])

    return Parsing_table


def main():
    input_file_name = "input3.txt"
    output_file_name = "output.txt"
    get_grammar(input_file_name, output_file_name)

#--------------------------------------------calculation of first-------------------------------------------------------

    flag = 0                                                    # to check if 1st iteration of for or not
    for ruletemp in grammar:                                    # read every line of grammar in rule
        rule = ruletemp.split()[1:]
        if rule[0][0] not in Non_Terminals:                     # Store only unique Non terminals
            Non_Terminals.append(rule[0][0])
            first_dict[rule[0][0]] = []                         # initialize dictionary key to corresponding non terminal and
                                                                # set the value of the key to a blank list
            if flag == 0:
                templist = []
                templist.append("$")
                follow_dict[rule[0][0]] = templist  # the follow of the starting production contains '$'
                flag = 1                                        # indicate that the 1st iteration of loop is done
            else:
                follow_dict[rule[0][0]] = []                    # initialize dictionary key to corresponding non terminal and
                                                                # set the value of the key to a blank list

        if rule[0][3].islower():                                # check to see if first character after '->' is a terminal if yes
            temp = []
            temp.append(rule[0][3])
            temp.append(ruletemp[0][0])
            first_dict[rule[0][0]].append(temp)           # add it to the first of Non terminal

    for ruletemp in grammar:                                        # read every line of grammar in rule
        rule = ruletemp.split()[1:]
        if rule[0][3].isupper():  # check to see if first character after '->' is a non-terminal if
            temp = copy.deepcopy(first_dict[rule[0][3]])
            for each in range(len(temp)):
                temp[each][1] = ruletemp[0][0]
            # first_dict[rule[0][0]] += first_dict[rule[0][3]]    # yes, add the first of the non terminal to first list
            first_dict[rule[0][0]] += temp

#---------------------------------------------calculation of follow-----------------------------------------------------

    for temp_temp_string in grammar:                                 # traverse through all the grammar rules
        temp_string = temp_temp_string.split()[1:]
        temp = list(temp_string[0])                             # convert each string(grammar rule) into a list
        for i in range(3, len(temp)):                           # traverse character wise through the grammar rule via temp list
            if temp[i] in Non_Terminals:                        # check if character temp[i] is a Non terminal or not
                if (i + 1) >= len(temp):                        # check if the Non terminal is in the last position of temp list
                    if temp[i] is not temp[0]:
                        follow_dict[temp[i]] += follow_dict[
                            temp[0]]  # add follow of left side non terminal to the follow of temp[i]
                else:
                    if temp[i + 1] in Non_Terminals:
                        follow_dict[temp[i]] += first_dict[temp[i + 1]]
                    else:
                        templist = []
                        templist.append(temp[i + 1])
                        follow_dict[temp[i]].append(
                            templist)  # the char after temp[i] is a terminal and is added to its follow

    write_dictionary(first_dict, "first", output_file_name)
    write_dictionary(follow_dict, "follow", output_file_name)

    Main_Parsing_Table = create_table()

    inputstring = "cccdd"

    flag = True
    inputstack = list(inputstring)
    inputstack.reverse()

    for each in inputstack:
        if each not in (Terminals or Non_Terminals):
            flag = False

    if flag:
        outputstack = []
        outputstack.append(grammar[0][2])

        while len(outputstack) > 0 and len(inputstack) > 0:
            print(outputstack)
            print(inputstack)
            print("----------------------")
            topofoutput = outputstack.pop()
            if topofoutput == inputstack[len(inputstack) - 1]:
                inputstack.pop()
                continue

            if topofoutput in Non_Terminals:
                ruleno = Main_Parsing_Table[non_terminal_dict[topofoutput]][
                    terminal_dict[inputstack[len(inputstack) - 1]]]
                if ruleno == -1:
                    print("Line 169: failed ! No rule exists !")
                    break

                temp = Parsing_Grammar[ruleno]

                if len(temp) > 1:
                    temp = list(temp)
                    temp.reverse()
                    for each in temp:
                        outputstack.append(each)
                else:
                    outputstack.append(Parsing_Grammar[ruleno])

            else:
                print("Line 174: Filed ! Cannot Proceed")

        if len(outputstack) == 0 and len(inputstack) == 0:
            print("Parsing Success !")
        else:
            print("Parsing failed !")

        print(inputstack)
        print(outputstack)
        # print(inputstack)
        # print(outputstack)

if __name__ == "__main__": main()