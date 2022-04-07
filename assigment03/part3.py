import boto3
import argparse
import botocore


"""დაწერეთ პროგრამა, რომელსაც არგუმენტებად გადაეცემა ბაკეტის სახელი,
გადმოსაწერი ფაილის სახელი და სადაც უნდა ჩაიწეროს ფაილი. პროგრამამ
მითითებული ბაკეტიდან უნდა გადმოწეროს გადმოსაწერი ფაილი და ჩაწეროს
დანიშნულების ფაილში. თუ პროგრამას არ გადაეცა არგუმენტი სადაც უნდა
ჩაიწეროს ფაილი, ნაგულისხმევად ჩაწეროს მიმდინარე დირექტორიაში."""


def init_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket')
    parser.add_argument('-f', '--file')
    parser.add_argument('-o', '--output')
    return parser.parse_args()


def download_file(
    client, file_name: str, bucket_name: str, output: str
) -> bool:
    try:
        client.meta.client.download_file(bucket_name, file_name, output)
        return True
    except botocore.exceptions.ClientError:
        return False


def main() -> None:
    parser = init_argparse()
    s3 = boto3.resource('s3')
    status = download_file(s3, parser.file, parser.bucket, parser.output)
    if status:
        print('file downloaded sucessfully')


if __name__ == '__main__':
    main()
