#!/usr/bin/env python3
import json
import argparse
from collections import OrderedDict


def split_testing_dataset(in_dev_source, in_dev_translated, out_dev, out_test, out_annot):

	print("Processing %s" % in_dev_translated)

	with open(in_dev_source) as original:
		original = json.load(original, object_hook=OrderedDict)

	with open(in_dev_translated) as f:
		f = json.load(f, object_hook=OrderedDict)

	global testing_set
	testing_set = {"version": f['version'], "data": []}
	annotator_source = {"version": original['version'], "data": []}  # This is only for the annotator!

	# choose 10 topics
	for i in range(10):
		# get title and 0th paragraph from each topic
		title, para = f['data'][i]['title'], f['data'][i]['paragraphs'][0]
		para_original = original['data'][i]['paragraphs'][0]
		
		#print("Please correct this paragraph: %s" % title)
		#print(json.dumps(para, indent=2))
		#para = json.loads(input("_"))

		# append to our new testing dataset and remove from dev
		f['data'][i]['paragraphs'] = f['data'][i]['paragraphs'][1:]
		testing_set['data'].append({"title": title, "paragraphs": [para]})

		annotator_source['data'].append({"title": title, "paragraphs": [para_original]})

		assert len(f['data'][i]['paragraphs']) > 0, "Only one paragraph: " + title

	# save
	with open(out_dev, "w") as fp:   json.dump(f, fp)
	with open(out_test, "w") as fp:  json.dump(testing_set, fp)
	with open(out_annot, "w") as fp: json.dump(annotator_source, fp)
	
	print("The new dev dataset %s was generated." % out_dev)
	print("The testing dataset %s was generated, now please perform manual correction." % out_test)


if __name__ == "__main__":
	argp = argparse.ArgumentParser()
	argp.add_argument("--in_dev_source", default="../squad2/dev-v2.0.json")
	argp.add_argument("--in_dev_translated", default="dev-v2.0.cs.json")
	argp.add_argument("--out_dev", default="dev-v2.0.cs.split.json")
	argp.add_argument("--out_test", default="test-v2.0.cs.raw.json")
	argp.add_argument("--out_annot", default="test-v2.0.en.json")
	args = argp.parse_args()
	split_testing_dataset(args.in_dev_source, args.in_dev_translated, args.out_dev, args.out_test, args.out_annot)

