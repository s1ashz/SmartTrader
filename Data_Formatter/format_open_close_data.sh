#!/usr/bin/env bash

echo "Current date: $(date)"

csv_file=$1
csv_file_dir="${csv_file%/*}"
csv_file_name="${csv_file##*/}"
csv_file_extension=${csv_file##*.}
csv_formatted_file="$csv_file_dir/formatted/$csv_file_name-f.$csv_file_extension"


first_line="true"
second_line="true"

res=$(awk -F "\"*,\"*" '{print $3}' $1)

row=($res)
next_open_value=${row[1]}


echo "Reading file....$csv_file and writing in file: $csv_formatted_file"
read_file() {
	IFS=,
	while read -ra a; do
		if [[ "${first_line}" == "true" ]];	then
			first_line="false"
			write_to_file "${a[*]}"
			continue
		fi
		if [[ "${second_line}" == "true" ]];	then
			second_line="false"
			write_to_file "${a[*]}"
			continue
		fi

		a[1]=$next_open_value
		#echo ${a[*]}
		next_open_value="${a[2]}"

		write_to_file "${a[*]}"
	done < $csv_file

}

write_to_file() {
	line=$1
	#echo "writing.....$line"
	echo $line | tr ' ' ',' >> $csv_formatted_file
}

read_file
echo "done"
