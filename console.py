#!/usr/bin/python3
"""implements the command interpreter for the AirBnB project"""
import cmd
import models
import re
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """implements the cmd for AirBnB"""

    prompt = "(hbnb) "
    classes = [
        'BaseModel', 'User','State', 'City',
        'Amenity', 'Place', 'Review'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__err_miss = "** class name missing **"
        self.__err_exist = "** class doesn't exist **"
        self.__err_id = "** instance id missing **"
        self.__err_inst = "** no instance found **"

    def precmd(self, line):
        pobj = re.compile(r'\w+\.\w+\(.*\)')
        if pobj.match(line):
            ln = ''
            p_cmd = re.compile(r'\.[a-zA-Z]+\(')
            p_class = re.compile(r'[a-zA-Z]+\.')
            p_args = re.compile(r'\(.*\)')
            c = p_class.search(line)
            if c:
                c = c.group()[:-1]
                ln = c

            command = p_cmd.search(line)
            if command:
                command = command.group()[1:-1]
                ln = command + ' ' + ln

            args = p_args.search(line)
            if args:
                args = args.group()[1:-1]
                self.__dic_rep = ''
                p_dic_rep = re.compile(r'\{.*\}')
                p_dic = p_dic_rep.search(args)
                if p_dic:
                    self.__dic_rep = p_dic.group()
                    args = args[:p_dic.start()]
                    args = args.strip()

                args = shlex.split(args)
                for i, e in enumerate(args):
                    if e[-1] == ',':
                        args[i] = e[:-1]

                args = shlex.join(args)
                ln = ln + ' ' + args

            line = ln

        self.__cmd_args = {str(i): e for i, e in enumerate(shlex.split(line))}
        return super().precmd(line)

    def emptyline(self):
        return False

    def help_help(self, line):
        print("\n".join(["Provides help on how to use the",
                         "available commands"
                         ]))

    def __check_errs(self, err_number):
        """checks if the cmd args is correct
        Args:
            line: the cmd args
            err_number: number errors to check for
        """
        if err_number >= 1:
            if self.__cmd_args.get('1', ''):
                if err_number == 1:
                    return True
            else:
                print(self.__err_miss)
                return False

        if err_number >= 2:
            if self.__cmd_args['1'] in self.classes:
                if err_number == 2:
                    return True
            else:
                print(self.__err_exist)
                return False

        if err_number >= 3:
            if self.__cmd_args.get('2', ''):
                if err_number == 3:
                    return True
            else:
                print(self.__err_id)
                return False

        if err_number >= 4:
            key = self.__cmd_args['1'] + '.' + self.__cmd_args['2']
            if key in models.storage.all():
                if err_number == 4:
                    return True

            else:
                print(self.__err_inst)
                return False

    def do_EOF(self, line):
        """EOF (^D) to exit the program"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program
        """
        return self.do_EOF(line)

    def do_create(self, _):
        """
        Creates new instance of BaseModel;
        Saves it (to the JSON file); and
        Prints its id
        """
        ret = self.__check_errs(2)
        if ret:
            model = eval(self.__cmd_args['1'])()
            model.save()
            print(model.id)

    def do_show(self, _):
        """
        prints the string representation of an instance based
        on the class name and id
        """
        ret = self.__check_errs(4)
        if ret:
            k = self.__cmd_args['1'] + '.' + self.__cmd_args['2']
            print(models.storage.all()[k])

    def do_destroy(self, _):
        """deletes an instance based on the class name and id"""
        ret = self.__check_errs(4)
        if ret:
            k = self.__cmd_args['1'] + '.' + self.__cmd_args['2']
            del models.storage.all()[k]
            models.storage.save()

    def do_all(self, _):
        """
        Prints all string representation of
        all instances based or not on the class name.
        """
        c = self.__cmd_args.get('1', '')
        objs = models.storage.all()
        if c:
            if c in self.classes:
                print([str(obj) for k, obj in objs.items() if k.startswith(c)])
            else:
                print(self.__err_exist)

        else:
            print([str(obj) for obj in objs.values()])

    def do_count(self, _):
        """counts the number of instances of a class"""
        ret = self.__check_errs(2)
        if ret:
            objs = models.storage.all()
            count = 0
            classes = [obj.to_dict()['__class__'] for obj in objs.values()]
            for e in classes:
                if e == self.__cmd_args['1']:
                    count += 1

            print(count)

    def do_update(self, _):
        """
        Updates an instance based on the class name and id
        by adding or updating attribute
        """
        ret = self.__check_errs(4)
        if ret:
            c = self.__cmd_args['1']
            k = c + '.' + self.__cmd_args['2']
            obj = models.storage.all()[k]
            if self.__dic_rep:
                for k, v in eval(self.__dic_rep).items():
                    if not k:
                        print("** attribute name missing **")
                    elif not v:
                        print("** value missing **")
                    else:
                        setattr(obj, k, v)
                        obj.save()
            else:
                attr_name = self.__cmd_args.get('3', '')
                attr_val = self.__cmd_args.get('4', '')
                if not attr_name:
                    print("** attribute name missing **")
                elif not attr_val:
                    print("** value missing **")
                else:
                    attr_val = self.parse(attr_val)
                    setattr(obj, attr_name, attr_val)
                    obj.save()

    @staticmethod
    def parse(s):
        """determines the type of s"""
        if s.isdigit():
            return int(s)
        elif s.replace('.', '1').isdigit():
            return float(s)

        return s

if __name__ == '__main__':
    HBNBCommand().cmdloop()
