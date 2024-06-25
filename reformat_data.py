#!/usr/bin/env python3
import argparse
import json
import os
import random
import string


def reformat_jsonl(input_file):
    output_file = input_file + ".tmp"

    content_keys = ["content"]
    try:
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            buffer = " "
            for idx, line in enumerate(infile):
                buffer += line.strip()
                if buffer:
                    try:
                        data = json.loads(line)
                        json.dump(data, outfile)
                        outfile.write('\n')
                        buffer = ""  # Clear buffer after successful parsing
                        #print(data)
                    except json.JSONDecodeError as e:
                        print(f"JSONDecodeError: {e}")
                        continue
            if buffer:
                try:
                    data = json.loads(buffer)
                    json.dump(data, outfile)
                    outfile.write('\n')
                except json.JSONDecodeError as e:
                    print(f"Error parsing remaining JSON: {buffer}")
                    print(f"JSONDecodeError: {e}")


                        

            if "functions" in data:
                data["tools"] = [{"function": func} for func in data["functions"]]
                del data["functions"]

            skip_sample = False
            if "messages" in data:
                for i, msg in enumerate(data["messages"]):
                    if "function_call" in msg:
                        if "content" in msg:
                            assert msg["content"] == ""
                            del msg["content"]

                        arguments = json.loads(msg["function_call"]["arguments"])
                        msg["function_call"]["arguments"] = json.dumps(arguments)

                        msg["tool_calls"] = [{"function": msg.pop("function_call")}]

                    for key in content_keys:
                        if key in msg and msg[key] == "":
                            if "tool_calls" in msg:
                                del msg[key]
                                print(
                                    f"Delete empty '{key}' field in tool call message in line {idx}"
                                )

                    if all(msg.get(key) in ["", None] for key in content_keys):
                        # conversation is incorrect
                        skip_sample = True

                    if msg["role"] in ["function", "tool"]:
                        msg["role"] = "tool"
                        if "tool_call_id" not in msg:
                            msg["tool_call_id"] = "".join(
                                random.choices(
                                    string.ascii_letters + string.digits, k=9
                                )
                            )

                        # make sure prev
                        if data["messages"][i - 1]["role"] == "assistant":
                            prev_msg = data["messages"][i - 1]
                            if "tool_calls" in prev_msg:
                                tool_name = prev_msg["tool_calls"][0]["function"][
                                    "name"
                                ]

                                assert tool_name == msg["name"]
                                prev_msg["tool_calls"][0]["id"] = msg["tool_call_id"]

                # make sure last message is an assistant message
                while (
                    len(data["messages"]) > 0
                    and data["messages"][-1]["role"] != "assistant"
                ):
                    data["messages"].pop()

                if len(data["messages"]) == 0:
                    skip_sample = True

            if not skip_sample:
                outfile.write(json.dumps(data) + "\n")
            else:
                print(f"Skipped {idx}th sample")

    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    os.rename(output_file, input_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reformat a JSONL file.")
    parser.add_argument("file", type=str, help="The input JSONL file")

    args = parser.parse_args()
    reformat_jsonl(args.file)
