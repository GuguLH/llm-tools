import os
import sys

TEMPLATE_INDEX = """library;

export './controller.dart';
export './view.dart';
"""

TEMPLATE_CONTROLLER = '''import 'package:get/get.dart';

class {ClassName}Controller extends GetxController {{

  {ClassName}Controller();

  _initData() {{
    update(["{id}"]);
  }}

  void onTap() {{

  }}

  @override
  void onReady() {{
    super.onReady();
    _initData();
  }}
}}
'''

TEMPLATE_VIEW = '''import 'package:flutter/material.dart';
import 'package:get/get.dart';
import './controller.dart';

class {ClassName}Page extends GetView<{ClassName}Controller> {{
  const {ClassName}Page({{super.key}});

  // 主视图
  Widget _buildView() {{
    return const Center(child: Text("{ClassName}Page"));
  }}

  @override
  Widget build(BuildContext context) {{
    return GetBuilder<{ClassName}Controller>(
      id: "{id}",
      init: {ClassName}Controller(),
      builder: (_) {{
        return Scaffold(
          appBar: AppBar(title: const Text("{id}")),
          body: SafeArea(child: _buildView()),
        );
      }},
    );
  }}
}}
'''


def create_getx_module(module_name: str):
    class_name = module_name.capitalize()
    base_path = os.path.join(os.getcwd(), module_name)
    os.makedirs(os.path.join(base_path, "widgets"), exist_ok=True)

    # index.dart
    with open(os.path.join(base_path, "index.dart"), "w", encoding="utf-8") as f:
        f.write(TEMPLATE_INDEX)

    # controller.dart
    with open(os.path.join(base_path, "controller.dart"), "w", encoding="utf-8") as f:
        f.write(TEMPLATE_CONTROLLER.format(ClassName=class_name, id=module_name))

    # view.dart
    with open(os.path.join(base_path, "view.dart"), "w", encoding="utf-8") as f:
        f.write(TEMPLATE_VIEW.format(ClassName=class_name, id=module_name))

    print(f"✅ Generated GetX module in '{base_path}'")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ 请传入模块名，例如: python gen_getx_module.py splash")
    else:
        create_getx_module(sys.argv[1])
