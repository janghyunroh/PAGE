import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart'; // .env를 위한 import 추가

class ApiService {
  // FastAPI 서버의 기본 URL입니다.
  // 실제 PC의 IP 주소를 사용해야 모바일 기기에서도 접속 가능합니다.
  // 예: 'http://192.168.1.10:8000'
  // 우선은 로컬 테스트를 위해 localhost를 사용합니다.
  static const String _baseUrl = 'http://127.0.0.1:8000';

  // .env 파일에서 API 키를 불러옵니다.
  // dotenv.env['변수명']! -> '!'는 이 값이 null이 아님을 보증합니다.
  static final String _apiKey = dotenv.env['PAGE_API_KEY']!;

  // 초안 생성을 요청하는 함수
  static Future<String> generateDraft(String topic) async {
    final url = Uri.parse('$_baseUrl/generate-draft');

    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          // 이제 .env에서 불러온 안전한 키를 사용합니다.
          'Authorization': 'Bearer $_apiKey',
        },
        // 요청 본문을 JSON 형식으로 인코딩합니다.
        body: jsonEncode({'topic': topic}),
      );

      if (response.statusCode == 200) {
        // 성공적으로 응답을 받으면, JSON을 디코딩하여 'draft' 값을 반환합니다.
        // UTF-8로 디코딩하여 한글 깨짐을 방지합니다.
        final responseBody = utf8.decode(response.bodyBytes);
        final data = jsonDecode(responseBody);
        return data['draft'];
      } else {
        // 에러가 발생하면 상태 코드와 에러 내용을 포함한 예외를 발생시킵니다.
        final errorBody = utf8.decode(response.bodyBytes);
        throw Exception(
          'Failed to generate draft. Status: ${response.statusCode}, Body: $errorBody',
        );
      }
    } catch (e) {
      // 네트워크 에러 등 예외 발생 시 처리
      throw Exception('Failed to connect to the server: $e');
    }
  }
}
