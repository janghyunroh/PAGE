import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart'; // .env를 위한 import 추가
import 'screens/home_screen.dart';

Future<void> main() async {
  // main 함수를 async로 변경하고, 앱 실행 전에 .env 파일을 로드합니다.
  await dotenv.load(fileName: ".env");
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'P.A.G.E.',
      theme: ThemeData(primarySwatch: Colors.blueGrey, useMaterial3: true),
      home: const HomeScreen(),
    );
  }
}
