import os
import re
import argparse
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from tqdm import tqdm
import io
from tabulate import tabulate
from typing import Optional, Callable
import json
import subprocess
from typing import Dict, List, Any
import os
import time
from datetime import datetime
import hashlib

# Add this function after the existing imports
def handle_git_operations(output_path: str) -> None:
    """
    Check if the output path is in a git repository and handle git operations.
    
    Args:
        output_path: Path where files were downloaded/created
    """
    try:
        # Check if we're in a git repository
        result = subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            cwd=output_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("Not in a git repository. Skipping git operations.")
            return

        # Get the repository root
        repo_root = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            cwd=output_path,
            capture_output=True,
            text=True
        ).stdout.strip()
        print(repo_root)


        # Add new files
        print("Adding new files to git...")
        subprocess.run(
            ['git', 'add', '.'],
            cwd=repo_root,
            check=True
        )

        # Commit changes
        print("Committing changes...")
        subprocess.run(
            ['git', 'commit', '-m', 'Add new downloaded and processed files'],
            cwd=repo_root,
            check=True
        )

        # Check if there's a remote repository
        remote_exists = subprocess.run(
            ['git', 'remote'],
            cwd=repo_root,
            capture_output=True,
            text=True
        ).stdout.strip()

        if remote_exists:
            print("Pulling latest changes from remote repository...")
            subprocess.run(
                ['git', 'pull', '--rebase'],
                cwd=repo_root,
                check=True
            )
            print("Pushing to remote repository...")
            subprocess.run(
                ['git', 'push'],
                cwd=repo_root,
                check=True
            )
            print("Successfully pushed to remote repository.")
        else:
            print("No remote repository found. Skipping push.")

    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {str(e)}")
    except Exception as e:
        print(f"An error occurred during git operations: {str(e)}")

class GoogleDriveDownloader:
    def __init__(self, credentials):
        """Initialize the Google Drive API client."""
        self.SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        
        if isinstance(credentials, dict):
            # Use credentials from environment variables
            credentials = service_account.Credentials.from_service_account_info(
                credentials, scopes=self.SCOPES)
        else:
            # Use credentials from file
            credentials = service_account.Credentials.from_service_account_file(
                credentials, scopes=self.SCOPES)
            
        self.service = build('drive', 'v3', credentials=credentials)

    def list_files(self):
        """List all accessible files in Google Drive."""
        try:
            results = self.service.files().list(
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, size)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return

            # Prepare table data
            table_data = []
            headers = ["ID", "Name", "Type", "Size (MB)"]
            
            for item in items:
                size = item.get('size', 'N/A')
                if size != 'N/A':
                    size = f"{int(size) / (1024*1024):.2f}"
                
                table_data.append([
                    item['id'],
                    item['name'],
                    item['mimeType'],
                    size
                ])

            # Print table
            print("\nAvailable files:")
            print(tabulate(table_data, headers=headers, tablefmt="grid"))

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def download_file(self, file_id: str, output_path: str, 
                     process_func: Optional[Callable] = None) -> Optional[str]:
        """
        Download a file from Google Drive and optionally process it.
        Handles both regular files and Google Workspace files.
        
        Args:
            file_id: The ID of the file to download
            output_path: Where to save the file
            process_func: Optional function to process the downloaded file
            
        Returns:
            The path to the downloaded file if successful, None otherwise
        """
        try:
            # Get file metadata
            file = self.service.files().get(fileId=file_id).execute()
            file_name = file.get('name')
            mime_type = file.get('mimeType', '')

            # Create output directory if it doesn't exist
            os.makedirs(output_path, exist_ok=True)

            # Define MIME type mappings for Google Workspace files
            GOOGLE_MIME_TYPES = {
                'application/vnd.google-apps.document': ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx'),
                'application/vnd.google-apps.spreadsheet': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx'),
                'application/vnd.google-apps.presentation': ('application/vnd.openxmlformats-officedocument.presentationml.presentation', '.pptx'),
                'application/vnd.google-apps.drawing': ('image/png', '.png'),
            }

            # Handle Google Workspace files
            if mime_type.startswith('application/vnd.google-apps'):
                if mime_type not in GOOGLE_MIME_TYPES:
                    print(f"Unsupported Google Workspace file type: {mime_type}")
                    return None

                export_mime_type, extension = GOOGLE_MIME_TYPES[mime_type]
                
                # Adjust filename to include proper extension
                base_name = os.path.splitext(file_name)[0]
                output_file = os.path.join(output_path, f"{base_name}{extension}")

                print(f"Exporting Google Workspace file as {extension}")
                request = self.service.files().export_media(
                    fileId=file_id,
                    mimeType=export_mime_type
                )
            else:
                # Handle regular files
                output_file = os.path.join(output_path, file_name)
                request = self.service.files().get_media(fileId=file_id)

            file_handle = io.BytesIO()
            downloader = MediaIoBaseDownload(file_handle, request)

            # Download the file with progress bar
            done = False
            with tqdm(total=100, desc=f"Downloading {file_name}") as pbar:
                previous_progress = 0
                while done is False:
                    status, done = downloader.next_chunk()
                    if status:
                        current_progress = int(status.progress() * 100)
                        pbar.update(current_progress - previous_progress)
                        previous_progress = current_progress

            # Empty the directory
            # output_directory = os.path.dirname(output_path)
            # existing_files = os.listdir(output_directory)
            # for file in existing_files:
            #     subprocess.run(['rm', file ], check=True, cwd=output_directory)
            # Save the file
            file_handle.seek(0)
            with open(output_file, 'wb') as f:
                f.write(file_handle.read())
            
            print(f"\nFile '{os.path.basename(output_file)}' downloaded successfully to {output_path}")

            # Process the file if a processing function is provided
            if process_func:
                print(f"Processing file: {os.path.basename(output_file)}")
                process_func(output_file)
                print("File processing completed")

            return output_file

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

def get_credentials_from_env():
    """Get credentials from environment variables."""
    required_keys = [
        'type', 'project_id', 'private_key_id', 'private_key',
        'client_email', 'client_id', 'auth_uri', 'token_uri',
        'auth_provider_x509_cert_url', 'client_x509_cert_url'
    ]
    
    creds = {}
    for key in required_keys:
        env_key = f"GOOGLE_DRIVE_{key.upper()}"
        value = os.environ.get(env_key)
        if not value:
            raise ValueError(f"Missing environment variable: {env_key}")
        creds[key] = value
    
    return creds


def segment_markdown_by_heading1(markdown):
    """
    Splits a markdown string into segments based on H1 headings.

    Args:
        markdown (str): The markdown string to segment.

    Returns:
        list: A list of segments, where each segment is a dictionary with a "title" and "content" key.
    """

    # Split the markdown by lines
    lines : List[str] = markdown.split('\n')

    # Initialize variables
    segments = []
    current_segment : List[str]= []

    # Iterate over the lines
    for line in lines:
        # If the line starts with an H1 heading
        if line.startswith('# '):
            # If there is a current segment, save it before starting a new one
            if current_segment:
                segments.append({
                    "title": current_segment[0].replace("# ", "").replace("**","").replace(" ","_").replace(",","_"),
                    "content": '\n'.join(current_segment)
                })
                current_segment = []

        # Add the line to the current segment
        current_segment.append(line)

    # Add the last segment if it exists
    if current_segment:
        segments.append({
            "title": current_segment[0].replace("# ", "").replace("**","").replace(" ","_").replace(",","_"),
            "content": '\n'.join(current_segment)
        })
        #.replaceAll("# ","").replaceAll("**","").replaceAll(" ","_").replaceAll(",","_")

    # Return the segments
    return segments

def process_file(file_path: str):
    """
    Process the downloaded file based on its type.
    Currently supports DOCX files, by brea
    
    Args:
        file_path: Path to the file to process
    """
    output_md = file_path + '.md'
    output_directory = os.path.dirname(file_path)
    media_output_directory = os.path.join(output_directory,"media")
    cache_file = os.path.join(output_directory, "cache.txt")



    subprocess.run(['pandoc', file_path, f"--extract-media=./" , '-o', output_md], check=True)
    print(f"File converted to Markdown and saved to: {output_md}")


    if os.path.exists(media_output_directory):
        subprocess.run(['rm', '-rf', media_output_directory], check=True)
    subprocess.run(['mv', "--force" , "./media", output_directory], check=True)
    print(f"Image directory moved to the output directory: {output_directory}/media")

    # Read the cache file if it exists
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cached_segments = set(f.read().splitlines())
    else:
        cached_segments = set()

    current_segments = set()

    with open(output_md, "r") as f :
        markdown_content = f.read().replace('.//media/image', '../media/image')

        # Remove patterns like {{width=... height=...}}
        markdown_content = re.sub(r'\{\{width=.*?height=.*?\}\}', '', markdown_content)

        # Remove patterns like {.underline}
        markdown_content = re.sub(r'\{\.\w+\}', '', markdown_content)

        print(markdown_content)
        segmentation = segment_markdown_by_heading1(markdown_content)

    for segment in segmentation :
        segment_file_path = os.path.join(output_directory,segment["title"]+".md")
        current_segments.add(segment_file_path)
        with open(segment_file_path, "w") as f :
            f.write(segment["content"])
            print(f"Segment saved as to: {segment['title']}")

    # Identify and remove files that are no longer needed
    files_to_remove = cached_segments - current_segments
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed outdated segment: {os.path.basename(file_path)}")

    # Update the cache file
    with open(cache_file, "w") as f:
        f.write("\n".join(current_segments))


    subprocess.run(['rm', file_path, output_md], check=True)



def get_file_metadata(service, file_id: str) -> Dict:
    """
    Get metadata for a specific file from Google Drive.
    
    Args:
        service: Google Drive service instance
        file_id: ID of the file to check
        
    Returns:
        Dict containing file metadata
    """
    try:
        return service.files().get(
            fileId=file_id,
            fields='id, name, modifiedTime, md5Checksum'
        ).execute()
    except Exception as e:
        print(f"Error getting file metadata: {str(e)}")
        return None

def watch_and_process(downloader: GoogleDriveDownloader, 
                     file_id: str, 
                     output_path: str, 
                     interval_minutes: int,
                     no_git: bool = False) -> None:
    """
    Watch a file for changes and process it when changes are detected.
    
    Args:
        downloader: GoogleDriveDownloader instance
        file_id: ID of the file to watch
        output_path: Where to save the downloaded file
        interval_minutes: How often to check for changes (in minutes)
        no_git: Whether to skip git operations
    """
    last_metadata = None
    
    print(f"\nStarting file watch mode...")
    print(f"Checking for changes every {interval_minutes} minutes")
    print("Press Ctrl+C to stop watching\n")

    while True:
        try:
            current_metadata = get_file_metadata(downloader.service, file_id)
            
            if not current_metadata:
                print("Failed to get file metadata. Retrying in next interval...")
                time.sleep(interval_minutes * 60)
                continue

            if last_metadata is None:
                # First run
                print(f"Initial file state recorded at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Watching file: {current_metadata.get('name')}")
                last_metadata = current_metadata
                
                # Process the file for the first time
                process_func = process_file if True else None
                downloaded_file = downloader.download_file(
                    file_id, 
                    output_path,
                    process_func
                )
                
                if downloaded_file and not no_git:
                    handle_git_operations(output_path)
                    
            else:
                # Check if file has changed
                current_modified = current_metadata.get('modifiedTime')
                last_modified = last_metadata.get('modifiedTime')
                
                if current_modified != last_modified:
                    print(f"\nChange detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"Processing updated file: {current_metadata.get('name')}")
                    
                    # Process the updated file
                    process_func = process_file if True else None
                    downloaded_file = downloader.download_file(
                        file_id, 
                        output_path,
                        process_func
                    )
                    
                    if downloaded_file and not no_git:
                        handle_git_operations(output_path)
                    
                    last_metadata = current_metadata
                else:
                    print(f"No changes detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", end='\r')

            # Wait for the specified interval
            time.sleep(interval_minutes * 60)
            
        except KeyboardInterrupt:
            print("\n\nFile watching stopped by user")
            break
        except Exception as e:
            print(f"\nAn error occurred while watching: {str(e)}")
            print("Retrying in next interval...")
            time.sleep(interval_minutes * 60)

# Modify the main function to include the watch feature
def main():
    parser = argparse.ArgumentParser(description='Google Drive File Downloader')
    parser.add_argument('action', choices=['list', 'get', 'watch'], 
                       help='Action to perform: list files, get a specific file, or watch a file for changes')
    parser.add_argument('--file-id', help='File ID to download or watch (required for get and watch actions)')
    parser.add_argument('--output', default='downloads',
                       help='Output directory for downloaded files')
    parser.add_argument('--credentials-file',
                       help='Path to service account credentials JSON file')
    parser.add_argument('--process', action='store_true',
                       help='Process the file after downloading')
    parser.add_argument('--no-git', action='store_true',
                       help='Skip git operations')
    parser.add_argument('--interval', type=int, default=5,
                       help='Interval in minutes between checks when watching (default: 5)')
    
    args = parser.parse_args()

    # Get credentials
    try:
        if args.credentials_file:
            credentials = args.credentials_file
        else:
            credentials = get_credentials_from_env()
    except Exception as e:
        print(f"Error with credentials: {str(e)}")
        return

    # Initialize downloader
    downloader = GoogleDriveDownloader(credentials)

    # Perform requested action
    if args.action == 'list':
        downloader.list_files()
    elif args.action == 'get':
        if not args.file_id:
            print("Error: --file-id is required for get action")
            return
        
        process_func = process_file if args.process else None
        downloaded_file = downloader.download_file(
            args.file_id, 
            args.output,
            process_func
        )
        
        if downloaded_file and not args.no_git:
            handle_git_operations(args.output)
    elif args.action == 'watch':
        if not args.file_id:
            print("Error: --file-id is required for watch action")
            return
        
        watch_and_process(
            downloader,
            args.file_id,
            args.output,
            args.interval,
            args.no_git
        )
if __name__ == '__main__':
    main()
