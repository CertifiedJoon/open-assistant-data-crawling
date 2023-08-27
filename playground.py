import json


classDefinitions = [
    {
        "Order": {
            "orderId": "String",
            "version": "Long",
            "orderType": "OrderType",
            "orderSide": "OrderSide",
            "status": "Status",
            "allocations": "List<Allocation>",
        }
    },
    {"OrderType": ["MarketOrderType", "LimitOrderType"]},
    {"MarketOrderType": ""},
    {"LimitOrderType": {"price": "Double"}},
    {"OrderSide": ["Buy", "Sell"]},
    {
        "Status": [
            "New",
            "Verifying",
            "Pending",
            "Working",
            "PartiallyFilled",
            "Filled",
            "Cancelled",
        ]
    },
    {"Allocation": ["LongAllocation", "EmptyAllocation"]},
    {"LongAllocation": {"clientName": "String"}},
    {"EmptyAllocation": ""},
]

statements = [
    "Order.",
    "Order.order",
    "Order.allocations.",
    "Status.P",
    "MarketOrderType.",
]

expectedOutput = {
    "Order.": ["allocations", "orderId", "orderSide", "orderType", "status"],
    "Order.order": ["orderId", "orderSide", "orderType"],
    "Order.allocations.": [""],
    "Status.P": ["PartiallyFilled", "Pending"],
    "MarketOrderType.": [""],
}

defined_classes = dict()

for definition_index in range(len(classDefinitions) - 1, -1, -1):
    object = classDefinitions[definition_index]
    defined_class_name = next(iter(object.keys()))
    defined_class = object[defined_class_name]
    if isinstance(defined_class, list):
        defined_classes[defined_class_name] = dict()
        for word in defined_class:
            if word not in defined_classes:
                defined_classes[defined_class_name][word] = ""
    elif isinstance(defined_class, str):
        defined_classes[defined_class_name] = ""
    elif isinstance(defined_class, dict):
        defined_classes[defined_class_name] = dict()
        for word, word_type in defined_class.items():
            if word_type in defined_classes:
                defined_classes[defined_class_name][word] = defined_classes[word_type]
            else:
                defined_classes[defined_class_name][word] = ""


print(json.dumps(defined_classes, indent=4))
import difflib

result = dict()

for statement in statements:
    result[statement] = []
    keys = statement.split(".")
    to_search = defined_classes
    for i, key in enumerate(keys):
        if i == len(keys) - 1:
            if key == "":
                if isinstance(to_search, dict):
                    result[statement].extend(sorted(list(to_search.keys()))[:5])
                elif isinstance(to_search, str):
                    result[statement].append(to_search)
            else:
                most_probable_keys = difflib.get_close_matches(
                    key, list(to_search.keys()), n=5, cutoff=(0.1 * min(6, len(key)))
                )
                result[statement].extend(sorted(most_probable_keys))
        else:
            most_probable_key = difflib.get_close_matches(
                key, list(to_search.keys()), n=1
            )[0]
            to_search = to_search[most_probable_key]

print(json.dumps(result, indent=4))
