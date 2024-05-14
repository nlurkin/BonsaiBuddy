import {
  Directive,
  EmbeddedViewRef,
  Input,
  TemplateRef,
  ViewContainerRef,
} from '@angular/core';

interface NgLetContext {
  ngLet: any;
  $implicit: any;
}

/**
 * This directive is similar to ngIf, but it renders the template even if the condition is false.
 */
@Directive({
  selector: '[ngLet]',
})
export class NgLetDirective {
  @Input()
  set ngLet(input: any) {
    this.context.ngLet = this.context.$implicit = input;
    this.updateContainer();
  }

  private context: NgLetContext = { ngLet: undefined, $implicit: undefined };
  private embeddedView: EmbeddedViewRef<NgLetContext> | undefined;

  constructor(
    private viewContainer: ViewContainerRef,
    private template: TemplateRef<NgLetContext>
  ) {}

  private updateContainer(): void {
    if (!this.embeddedView)
      this.embeddedView = this.viewContainer.createEmbeddedView(
        this.template,
        this.context
      );
  }
}
