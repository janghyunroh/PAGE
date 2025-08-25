import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _topicController = TextEditingController();
  String _generatedDraft = '';
  bool _isLoading = false;
  String? _errorMessage;

  Future<void> _handleGenerateDraft() async {
    if (_topicController.text.isEmpty) {
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _generatedDraft = '';
    });

    try {
      final draft = await ApiService.generateDraft(_topicController.text);
      setState(() {
        _generatedDraft = draft;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('P.A.G.E. - AI 초안 생성기'),
        backgroundColor: Colors.blueGrey[900],
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 주제 입력 필드
            TextField(
              controller: _topicController,
              decoration: const InputDecoration(
                labelText: '블로그 글의 주제를 입력하세요',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            // 초안 생성 버튼
            ElevatedButton.icon(
              onPressed: _isLoading ? null : _handleGenerateDraft,
              icon: const Icon(Icons.auto_awesome),
              label: const Text('초안 생성하기'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                textStyle: const TextStyle(fontSize: 16),
              ),
            ),
            const SizedBox(height: 24),
            const Divider(),
            const SizedBox(height: 16),
            // 결과 표시 영역
            Expanded(child: _buildResultView()),
          ],
        ),
      ),
    );
  }

  // 로딩, 에러, 성공 상태에 따라 다른 위젯을 보여주는 함수
  Widget _buildResultView() {
    if (_isLoading) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(),
            SizedBox(height: 16),
            Text('AI가 초안을 작성 중입니다...'),
          ],
        ),
      );
    }
    if (_errorMessage != null) {
      return Center(
        child: Text(
          '에러 발생:\n$_errorMessage',
          style: const TextStyle(color: Colors.red),
          textAlign: TextAlign.center,
        ),
      );
    }
    if (_generatedDraft.isEmpty) {
      return const Center(child: Text('여기에 생성된 초안이 표시됩니다.'));
    }
    // Markdown 텍스트를 위젯으로 렌더링
    return Markdown(
      data: _generatedDraft,
      selectable: true,
      styleSheet: MarkdownStyleSheet(
        h1: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        p: const TextStyle(fontSize: 16, height: 1.5),
      ),
    );
  }
}
