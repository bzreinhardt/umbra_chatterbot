from django_chatterbot.data_parsing import InputParser


def input_parser_test():
	ip = InputParser()
	test_string = "I did 10 pushups"
	test_out = ip.find_noun_number_pair(test_string)
	print "input parser out = "
	print test_out

def internal_parser_test():
	ip = InputParser()
	test_string = "pushups:10:hard:sweaty"
	test_out = ip.find_key_value_pair(test_string)
	print "input parser out = "
	print test_out

if __name__ == '__main__':
	input_parser_test()
	internal_parser_test()