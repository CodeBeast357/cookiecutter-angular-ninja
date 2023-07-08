import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';


export interface blogPostItem {
  id: number;
  title: string;
  body: string;
}

export interface blogPostPayload {
  title: string;
  body: string;
}

export interface blogPostResponse {
  items: blogPostItem[];
  count: number;
}
@Component({
  selector: 'app-blog-post-list',
  templateUrl: './blog-post-list.component.html',
  styleUrls: ['./blog-post-list.component.scss']
})
export class BlogPostListComponent implements OnInit {

  blogPosts: blogPostItem[] = [];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.getBlogPosts();
  }

  getBlogPosts() {
    this.http.get<blogPostResponse>('/api/blog_posts/?page=1').subscribe(
      (data: blogPostResponse) => {
        console.log('response: ', data)
        this.blogPosts = data.items;
      }
    )
  }

  createBlogPost() {
    this.http.post<blogPostItem>('/api/blog_posts/', {title: 'This is a new post', body: "This is some body baby"}).subscribe(
      (data: blogPostItem) => {
        console.log('response: ', data)
        this.blogPosts.push(data);
      }
    )
  }

}
