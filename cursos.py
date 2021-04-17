import sqlite3 as sql


class Table:
    def __init__(self):
        self.con = sql.connect('cadastro.db')
        self.cur = self.con.cursor()

    def create_table(self):
        infor = Table.input_create(self)
        sql_create = 'create table if not exists cursos ('
        for c in range(0, len(infor[0])):
            if c == 0:
                sql_create += f'{infor[c][c]} primary key'
            else:
                sql_create += f' {infor[0][c]} {infor[1][c]}'
            if c < (len(infor[0])-1):
                sql_create += ','
        sql_create += ')'
        self.cur.execute(sql_create)

    def insert_table(self):
        registers = Table.input_insert(self)
        for register in registers:
            sql_insert = 'insert into cursos values ' + register
            print(sql_insert)
            self.cur.execute(sql_insert)
            self.con.commit()

    def select_table(self):
        infor = Table.input_select(self)
        shower = ''
        for elem in infor['shower']:
            shower += elem
        sql_select = f'select {shower} from cursos order by {infor["order"]}'
        self.cur.execute(sql_select)
        dados = self.cur.fetchall()
        for linha in dados:
            print(linha)

    def update_table(self):
        infor = Table.input_update(self)
        for c in range(0, len(infor[0])):
            sql_update = f"update cursos set nome = '{infor[0][c]}' where idcurso = {infor[1][c]}"
            self.cur.execute(sql_update)
            self.con.commit()

    def delete_table(self):
        infor = Table.input_delete(self)
        for c in range(0, len(infor)):
            sql_delete = f'delete from cursos where idcurso = {infor[c]}'
            self.cur.execute(sql_delete)

    def drop_table(self):
        answer = input(' -Deseja apagar tabela?[S/N]: ').upper().strip()
        if answer in 'SN':
            if answer == 'S':
                sql_drop = 'drop table cursos'
                self.cur.execute(sql_drop)
            else:
                return None

    def input_update(self):
        c = 0
        nome_curso = [input('Nome do novo curso: ')]
        id_curso = [input('Id do curso antigo: ')]
        while True:
            if c > 0:
                answer = str(input('Fazer outra alteração?[S/N] ')).strip().upper()
                if answer == 'S':
                    nome_curso.append(input('Nome do novo curso: '))
                    id_curso.append(input('Id do curso antigo: '))
                else:
                    break
            c += 1
        return nome_curso, id_curso

    def input_delete(self):
        c = 0
        id_curso = [int(input('Id do curso à remover: '))]
        while True:
            if c > 0:
                answer = str(input('Fazer outra alteração?[S/N] ')).strip().upper()
                if answer == 'S':
                    id_curso.append(int(input('Id do curso à remover: ')))
                else:
                    break
            c += 1
        return id_curso

    def input_create(self):
        Table.options_create(self)
        c = 0
        attributes = [str(input('Nome do atributo: '))]
        config = [int(input('Tipo primitivo: '))]
        while True:
            answer = str(input('Deseja continuar[S/N]:')).strip().upper()
            if answer in 'SN':
                if answer == 'S':
                    attributes.append(input('Nome do atributo: '))
                    config.append(int(input('Tipo primitivo: ')))
                elif answer == 'N':
                    break
            else:
                print('\033[1;91mResposta INVÁLIDA!\033[m, \033[91mDigite novamente!\033[m')
                print()
        c += 1
        for c in range(0, len(config)):
            if config[c] == 1:
                config.insert(c, 'int')
                config.remove(1)
            elif config[c] == 2:
                config.insert(c, 'tinyint')
                config.remove(2)
            elif config[c] == 3:
                config.insert(c, 'bigint')
                config.remove(3)
            elif config[c] == 4:
                config.insert(c, 'decimal')
                config.remove(4)
            elif config[c] == 5:
                config.insert(c, 'varchar(30)')
                config.remove(5)
            elif config[c] == 6:
                config.insert(c, 'text')
                config.remove(6)
            elif config[c] == 7:
                config.insert(c, 'enum')
                config.remove(7)
            elif config[c] == 8:
                config.insert(c, 'date')
                config.remove(8)
            elif config[c] == 9:
                config.insert(c, 'time')
                config.remove(9)
            elif config[c] == 10:
                config.insert(c, 'year')
                config.remove(10)

        return attributes, config

    def input_insert(self):
        name_arq = input('Nome do arquivo: ')
        arq = open(f'{name_arq}.txt', 'r+', encoding='utf-8')
        records = arq.readlines()
        for index in range(0, len(records)):
            records[index] = records[index].rstrip('\n')
        arq.close()
        return records

    def input_select(self):
        attributs = tuple(input('Atributos para análise: ').split())
        order = input('Ordernar por: ')
        infors = {'shower': attributs, 'order': order}
        return infors

    def options_create(self):
        print(f'Tipos NUMÉRICOS:{"|":>3}{"Tipos STRINGS:":>16}{"|":>3}{"Tipos DATA e HORA:":>20}{"|":>2}')
        print(f' [1]Int{"|":>12}{"[5]Varchar":>13}{"|":>6}{"[8]Date":>10}{"|":>12}')
        print(f' [2]Tinyint{"|":>8}{"[6]Text":>10}{"|":>9}{"[9]Time":>10}{"|":>12}')
        print(f' [3]Bigint{"|":>9}{"[7]Enum":>10}{"|":>9}{"[10]Year":>11}{"|":>11}')
        print(f' [4]Decimal{"|":>8}{"|":>19}{"|":>22}')
        print('-' * 60)


def main():
    if __name__ == '__main__':
        table = Table()
        while True:
            print(f'{"MENU":-^25}\n {"[0]Sair"}')
            print(f'{" [1]Criar tabela"}\n {"[2]Inserir dado"}\n {"[3]Apagar dado"}\n '
                  f'{"[4]Mudar dado"}\n {"[5]Mostrar tabela"}\n {"[6]Apagar tabela"}')
            print('-' * 25)
            opc = int(input('Sua opção: '))
            if (opc > 6) or (opc < 0):
                print('\033[1;91mOpção INVÁLIDA!\033[m \033[91mtente novamente\033[m')
            if opc == 1:
                table.create_table()
            elif opc == 2:
                table.insert_table()
            elif opc == 3:
                table.delete_table()
            elif opc == 4:
                table.update_table()
            elif opc == 5:
                table.select_table()
            elif opc == 6:
                table.drop_table()
            elif opc == 0:
                print(f'{"<<ATÉ LOGO>>":^25}')
                table.cur.close()
                table.con.close()
                break


main()
