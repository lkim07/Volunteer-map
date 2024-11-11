import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';

// JobService class to fetch jobs from the Flask API
class JobService {
  final String apiUrl = 'http://127.0.0.1:5000/jobs';

  Future<Map<String, dynamic>> fetchJobs() async {
    final response = await http.get(Uri.parse(apiUrl));

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load jobs');
    }
  }
}

// Function to launch a URL in the browser (rename to avoid conflict with url_launcher)
void launchUrl(String url) async {
  if (await canLaunchUrl(Uri.parse(url))) {
    await launch(url); // Use url_launcher's launch function here
  } else {
    throw 'Could not launch $url';
  }
}

// JobListScreen displays the list of jobs
class JobListScreen extends StatefulWidget {
  const JobListScreen({super.key});

  @override
  _JobListScreenState createState() => _JobListScreenState();
}

class _JobListScreenState extends State<JobListScreen> {
  late Future<Map<String, dynamic>> futureJobs;

  @override
  void initState() {
    super.initState();
    futureJobs = JobService().fetchJobs(); // Fetch jobs when the screen loads
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Volunteer Jobs'),
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: futureJobs,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No jobs found.'));
          } else {
            final jobs = snapshot.data!;
            return ListView(
              children: jobs.entries.map((entry) {
                final city = entry.key;
                final cityJobs = entry.value as List<dynamic>;
                return ExpansionTile(
                  title: Text(city),
                  children: cityJobs.map((job) {
                    return ListTile(
                      title: Text(job['title']),
                      subtitle: Text(job['location']),
                      onTap: () => launchUrl(
                          job['link']), // Use the updated function name here
                    );
                  }).toList(),
                );
              }).toList(),
            );
          }
        },
      ),
    );
  }
}

// Main entry point of the app
void main() {
  runApp(const MyApp());
}

// Main app widget
class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        textTheme: const TextTheme(
          titleLarge: TextStyle(
            color: Colors.red,
          ),
        ),
      ),
      home: const JobListScreen(), // Set the home screen to JobListScreen
    );
  }
}
