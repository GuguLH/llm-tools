import 'package:get/get.dart';

class HomeController extends GetxController {

  HomeController();

  _initData() {
    update(["home"]);
  }

  void onTap() {

  }

  @override
  void onReady() {
    super.onReady();
    _initData();
  }
}
